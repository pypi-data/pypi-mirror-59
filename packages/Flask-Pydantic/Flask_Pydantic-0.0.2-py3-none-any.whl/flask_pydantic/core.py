from functools import wraps
from typing import Optional, Callable, TypeVar, Any, Union, Iterable, Type

from flask import request, jsonify, make_response, Response
from pydantic import BaseModel, ValidationError

from .exceptions import InvalidIterableOfModelsException

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass


InputParams = TypeVar("InputParams")


def make_json_response(
    content: Union[BaseModel, Iterable[BaseModel]],
    status_code: int,
    exclude_none: bool = False,
    many: bool = False,
) -> Response:
    """serializes model, creates JSON response with given status code"""
    if many:
        js = f"[{', '.join([model.json(exclude_none=exclude_none) for model in content])}]"
    else:
        js = content.json(exclude_none=exclude_none)
    response = make_response(js, status_code)
    response.mimetype = "application/json"
    return response


def is_iterable_of_models(response_content: Any) -> bool:
    try:
        return all(isinstance(obj, BaseModel) for obj in response_content)
    except TypeError:
        return False


def validate(
    body: Optional[Type[BaseModel]] = None,
    query: Optional[Type[BaseModel]] = None,
    on_success_status: int = 200,
    exclude_none: bool = False,
    response_many: bool = False,
):
    """
    Decorator for route methods which will validate query and body parameters as well as
    serialize the response (if it derives from pydantic's BaseModel class).

    `exclude_none` whether to remove None fields from response
    `response_many` whether content of response consists of many objects
        (e. g. List[BaseModel]). Resulting response will be an array of serialized
        models.


    example:

    from flask import request
    from flask_pydantic import validate
    from pydantic import BaseModel

    class Query(BaseModel):
        query: str

    class Body(BaseModel):
        color: str

    class MyModel(BaseModel):
        id: int
        color: str
        description: str

    ...

    @app.route("/")
    @validate(query=Query, body=Body)
    def test_route():
        query = request.query_params.query
        color = request.body_params.query

        return MyModel(...)

    -> that will render JSON response with serialized MyModel instance
    """

    def decorate(func: Callable[[InputParams], Any]) -> Callable[[InputParams], Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            query_params = request.args
            body_params = request.get_json()
            q, b, err = None, None, {}
            if query:
                try:
                    q = query(**query_params)
                except ValidationError as ve:
                    err["query_params"] = ve.errors()
            if body:
                try:
                    b = body(**body_params)
                except ValidationError as ve:
                    err["body_params"] = ve.errors()
            request.query_params = q
            request.body_params = b
            if err:
                return make_response(jsonify({"validation_error": err}), 400)
            res = func(*args, **kwargs)

            if response_many:
                if is_iterable_of_models(res):
                    return make_json_response(
                        res, on_success_status, exclude_none, True
                    )
                else:
                    raise InvalidIterableOfModelsException(res)

            if isinstance(res, BaseModel):
                return make_json_response(
                    res, on_success_status, exclude_none=exclude_none
                )

            if (
                isinstance(res, tuple)
                and len(res) == 2
                and isinstance(res[0], BaseModel)
            ):
                return make_json_response(res[0], res[1], exclude_none=exclude_none)

            return res

        return wrapper

    return decorate
