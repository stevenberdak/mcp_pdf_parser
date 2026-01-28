from abc import ABC, abstractmethod
from ..context.schema import ModelContext
from ..protocol.formats import Answer

class ModelAdapter(ABC):
    @abstractmethod
    def generate(self, ctx: ModelContext) -> Answer:
        raise NotImplementedError
