from math import ceil
from typing import Optional, Any, TypeVar, Generic, Sequence

from fastapi_pagination import Params, Page
from fastapi_pagination.bases import BasePage, AbstractParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero

from schemas.job import JobCategory

T = TypeVar("T")


class Page(BasePage[T], Generic[T]):
    page: GreaterEqualOne
    size: GreaterEqualOne
    pages: Optional[GreaterEqualZero] = None
    categories: Optional[dict] = None,

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        pages = ceil(total / params.size) if total is not None else None

        return cls(
            total=total,
            items=items,
            page=params.page,
            size=params.size,
            pages=pages,
            categories={category.name: category.value for category in JobCategory},
            **kwargs,
        )
