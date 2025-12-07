from decimal import Decimal
from pydantic import BaseModel

from enums.cryptocurrency import Cryptocurrency
from enums.withdraw_type import WithdrawType


class WithdrawalDTO(BaseModel):
    withdrawType: WithdrawType
    cryptoCurrency: Cryptocurrency
    toAddress: str
    txIdList: list = []
    receivingAmount: Decimal | None = None
    blockchainFeeAmount: Decimal | None = None
    serviceFeeAmount: Decimal | None = None
    onlyCalculate: bool
    totalWithdrawalAmount: Decimal | None = None
