"""Domain value objects."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re


@dataclass(frozen=True)
class Address:
    """Address value object."""

    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    country: str = "Brasil"

    def __str__(self):
        parts = [f"{self.street}, {self.number}"]
        if self.complement:
            parts.append(self.complement)
        parts.append(f"{self.neighborhood}")
        parts.append(f"{self.city}/{self.state}")
        parts.append(self.zip_code)
        return ", ".join(parts)


@dataclass(frozen=True)
class CNPJ:
    """CNPJ value object with validation."""

    value: str

    def __post_init__(self):
        if not self._validate(self.value):
            raise ValueError(f"CNPJ inválido: {self.value}")

    @staticmethod
    def _validate(cnpj: str) -> bool:
        cnpj = re.sub(r"[^\d]", "", cnpj)
        if len(cnpj) != 14:
            return False
        return True

    def __str__(self):
        return f"{self.value[:2]}.{self.value[2:5]}.{self.value[5:8]}/{self.value[8:12]}-{self.value[12:]}"


@dataclass(frozen=True)
class CPF:
    """CPF value object with validation."""

    value: str

    def __post_init__(self):
        if not self._validate(self.value):
            raise ValueError(f"CPF inválido: {self.value}")

    @staticmethod
    def _validate(cpf: str) -> bool:
        cpf = re.sub(r"[^\d]", "", cpf)
        if len(cpf) != 11:
            return False
        return True

    def __str__(self):
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"


@dataclass(frozen=True)
class Money:
    """Money value object."""

    amount: float
    currency: str = "BRL"

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Moedas diferentes")
        return Money(self.amount + other.amount, self.currency)


@dataclass(frozen=True)
class DateRange:
    """Date range value object."""

    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Data inicial maior que final")

    @property
    def days(self) -> int:
        return (self.end - self.start).days

    def contains(self, date: datetime) -> bool:
        return self.start <= date <= self.end


@dataclass(frozen=True)
class TrackingNumber:
    """Tracking number value object."""

    value: str
    carrier_code: str

    def __str__(self):
        return self.value
