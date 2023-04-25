from .models import Balance as BalanceModel


class BalanceHandler:
    def get_user_balance(user_id):
        try:
            balance_obj = BalanceModel.objects.get(user=user_id)
            return balance_obj
        except BalanceModel.DoesNotExist:
            return None

    def get(self, user_id):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            return balance_obj.balance

        return None

    def set(self, user_id, new_value):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            balance_obj.balance = new_value
            balance_obj.save()

        return None

    def increase(self, user_id, increased_value):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            balance_obj.balance += increased_value
            balance_obj.save()

    def decrease(self, user_id, increased_value):
        balance_obj = self.get_user_balance(user_id)
        if balance_obj is not None:
            balance_obj.balance -= increased_value
            balance_obj.save()
