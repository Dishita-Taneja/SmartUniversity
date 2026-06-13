class Fee:
    def __init__(self, student_id, total_fee):
        self.student_id = student_id
        self.total_fee = total_fee
        self.paid_fee = 0
        self.balance_fee = total_fee

    def pay_fee(self, amount):
        if amount <= 0:
            raise ValueError("Invalid payment amount.")
        if amount > self.balance_fee:
            raise ValueError("Payment exceeds balance fee.")
        self.paid_fee += amount
        self.balance_fee -= amount
        return f"Payment of {amount} successful. Remaining balance: {self.balance_fee}"

    def check_balance(self):
        return self.balance_fee

    def generate_receipt(self):
        return {
            "student_id": self.student_id,
            "total_fee": self.total_fee,
            "paid_fee": self.paid_fee,
            "balance_fee": self.balance_fee
        }

    def __str__(self):
        return f"Fee(Student: {self.student_id}, Balance: {self.balance_fee})"

    def __repr__(self):
        return f"Fee(student_id={self.student_id}, total={self.total_fee}, paid={self.paid_fee})"
