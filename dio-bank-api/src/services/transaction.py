from databases.interfaces import Record
from decimal import Decimal
from typing import Optional

from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
    async def read_all(self, account_id: int, limit: int, skip: int = 0) -> list[Record]:
        query = transactions.select().where(transactions.c.account_id == account_id).limit(limit).offset(skip)
        return await database.fetch_all(query)

    @database.transaction()
    async def create(self, transaction: TransactionIn) -> Optional[Record]:
        # Buscar conta
        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)
        
        if not account:
            raise AccountNotFoundError(f"Account {transaction.account_id} not found")

        # CORREÇÃO: Acessar campos do Record usando notação de dicionário
        try:
            current_balance = Decimal(str(account["balance"])) if account["balance"] is not None else Decimal('0')
            transaction_amount = Decimal(str(transaction.amount))
        except (ValueError, TypeError, KeyError) as e:
            raise BusinessError(f"Invalid amount format: {e}")

        # Calcular novo saldo
        if transaction.type == TransactionType.WITHDRAWAL:
            new_balance = current_balance - transaction_amount
            if new_balance < 0:
                raise BusinessError("Operation not carried out due to lack of balance")
        else:
            new_balance = current_balance + transaction_amount

        try:
            # Registrar transação
            transaction_id = await self.__register_transaction(transaction)
            if not transaction_id:
                raise BusinessError("Failed to create transaction record")

            # Atualizar saldo da conta
            await self.__update_account_balance(transaction.account_id, float(new_balance))

            # Buscar transação criada
            query = transactions.select().where(transactions.c.id == transaction_id)
            created_transaction = await database.fetch_one(query)
            
            if not created_transaction:
                raise BusinessError("Failed to retrieve created transaction")
                
            return created_transaction

        except Exception as e:
            raise BusinessError(f"Transaction failed: {str(e)}")

    async def __update_account_balance(self, account_id: int, balance: float) -> None:
        try:
            command = accounts.update().where(accounts.c.id == account_id).values(balance=balance)
            result = await database.execute(command)
            if result is None:
                raise BusinessError(f"Failed to update account {account_id} balance")
        except Exception as e:
            raise BusinessError(f"Error updating account balance: {str(e)}")

    async def __register_transaction(self, transaction: TransactionIn) -> Optional[int]:
        try:
            command = transactions.insert().values(
                account_id=transaction.account_id,
                type=transaction.type,
                amount=float(transaction.amount),  # Converter para float
            )
            transaction_id = await database.execute(command)
            return transaction_id
        except Exception as e:
            raise BusinessError(f"Error registering transaction: {str(e)}")