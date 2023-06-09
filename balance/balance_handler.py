from .models import Balance as BalanceModel


class BalanceHandler:
    # private
    def _user_balance(self, user):
        try:
            return BalanceModel.objects.get(user=user)
        except BalanceModel.DoesNotExist:
            return None

    def get(self, user_id):
        balance_obj = self._user_balance(user=user_id)
        return balance_obj if balance_obj is not None else None

    def set(self, user_id, new_value):
        balance_obj = self._user_balance(user=user_id)
        if balance_obj is not None:
            balance_obj.balance = new_value
            balance_obj.save()

        return None

    def increase(self, user_id, increased_value):
        balance_obj = self._user_balance(user=user_id)
        if balance_obj is not None:
            balance_obj.balance += increased_value
            balance_obj.save()

    def decrease(self, user_id, decreased_value):
        balance_obj = self._user_balance(user=user_id)
        if balance_obj is not None:
            balance_obj.balance -= decreased_value
            balance_obj.save()

    def is_enough(self, user_id, value):
        balance_obj = self._user_balance(user=user_id)
        return balance_obj is not None and balance_obj.balance >= value
