from .models import Balance as BalanceModel


class BalanceHandler:
    def get_user_balance(user_id):
        try:
            balance_obj = BalanceModel.objects.get(user=user_id)
            return balance_obj
        except BalanceModel.DoesNotExist:
            return None

    def increase(self, user_id, increased_value):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            balance_obj.balance += increased_value

    def decrease(self, user_id, increased_value):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            balance_obj.balance -= increased_value
