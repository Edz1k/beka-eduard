import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# === 1. OOP-часть ===

class Employee:
    def __init__(self, name: str, position: str, base_salary: float):
        self._name = name
        self._position = position
        self._base_salary = base_salary

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @property
    def base_salary(self):
        return self._base_salary

    def __str__(self):
        return f"{self._name} ({self._position})"

class Manager(Employee):
    def __init__(self, name: str, base_salary: float, bonus: float):
        super().__init__(name, "Manager", base_salary)
        self._bonus = bonus

    @property
    def bonus(self):
        return self._bonus

class Engineer(Employee):
    def __init__(self, name: str, base_salary: float,
                 overtime_hours: float, overtime_rate: float):
        super().__init__(name, "Engineer", base_salary)
        self._overtime_hours = overtime_hours
        self._overtime_rate = overtime_rate

    @property
    def overtime_hours(self):
        return self._overtime_hours

    @property
    def overtime_rate(self):
        return self._overtime_rate

class PayrollSystem(ABC):
    @abstractmethod
    def calculate_payroll(self) -> dict[Employee, float]:
        pass

class CompanyPayroll(PayrollSystem):
    def __init__(self):
        self._employees: list[Employee] = []

    def add_employee(self, emp: Employee):
        self._employees.append(emp)

    def remove_employee(self, index: int):
        self._employees.pop(index)

    def list_employees(self):
        return list(self._employees)

    def calculate_payroll(self) -> dict[Employee, float]:
        payroll = {}
        for emp in self._employees:
            if isinstance(emp, Manager):
                total = emp.base_salary + emp.bonus
            elif isinstance(emp, Engineer):
                total = emp.base_salary + emp.overtime_hours * emp.overtime_rate
            else:
                total = emp.base_salary
            payroll[emp] = total
        return payroll

# === 2. GUI на Tkinter ===

class PayrollApp:
    def __init__(self, master):
        self.master = master
        master.title("Система расчёта зарплат")
        master.geometry("650x600")
        self.company = CompanyPayroll()

        # Переменные формы
        self.emp_type_var = tk.StringVar(value="Manager")
        self.name_var = tk.StringVar()
        self.base_salary_var = tk.StringVar()
        self.bonus_var = tk.StringVar()
        self.overtime_hours_var = tk.StringVar()
        self.overtime_rate_var = tk.StringVar()

        self._build_widgets()
        self._update_form_fields()

    def _build_widgets(self):
        frm = ttk.LabelFrame(self.master, text="Добавить сотрудника")
        frm.pack(fill="x", padx=10, pady=10)

        # Тип сотрудника
        ttk.Label(frm, text="Тип:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.OptionMenu(frm, self.emp_type_var, "Manager", "Manager", "Engineer",
                       command=lambda e: self._update_form_fields())\
            .grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Общее: имя, база
        ttk.Label(frm, text="Имя:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frm, textvariable=self.name_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frm, text="База (₸):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frm, textvariable=self.base_salary_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Параметры для Manager
        self.bonus_label = ttk.Label(frm, text="Бонус (₸):")
        self.bonus_entry = ttk.Entry(frm, textvariable=self.bonus_var)

        # Параметры для Engineer
        self.oh_label = ttk.Label(frm, text="Сверхурочные (ч):")
        self.oh_entry = ttk.Entry(frm, textvariable=self.overtime_hours_var)
        self.or_label = ttk.Label(frm, text="Тариф (₸/ч):")
        self.or_entry = ttk.Entry(frm, textvariable=self.overtime_rate_var)

        # Кнопка добавления
        ttk.Button(frm, text="Добавить", command=self._add_employee)\
            .grid(row=6, column=0, columnspan=2, pady=10)

        # Список сотрудников
        lf = ttk.LabelFrame(self.master, text="Сотрудники")
        lf.pack(fill="both", expand=True, padx=10, pady=5)
        self.emp_listbox = tk.Listbox(lf)
        self.emp_listbox.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        sb = ttk.Scrollbar(lf, orient="vertical", command=self.emp_listbox.yview)
        sb.pack(side="right", fill="y", padx=(0,5), pady=5)
        self.emp_listbox.config(yscrollcommand=sb.set)

        ttk.Button(self.master, text="Удалить выбранного", command=self._remove_selected)\
            .pack(pady=5)
        ttk.Button(self.master, text="Рассчитать зарплаты", command=self._show_payroll)\
            .pack(pady=5)

        # Поле вывода зарплат
        self.payroll_text = tk.Text(self.master, height=10)
        self.payroll_text.pack(fill="both", expand=False, padx=10, pady=5)

    def _update_form_fields(self):
        # Сначала убираем всё
        for w in (self.bonus_label, self.bonus_entry,
                  self.oh_label, self.oh_entry,
                  self.or_label, self.or_entry):
            w.grid_forget()

        if self.emp_type_var.get() == "Manager":
            self.bonus_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.bonus_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        else:
            self.oh_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.oh_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
            self.or_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
            self.or_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    def _add_employee(self):
        name = self.name_var.get().strip()
        try:
            base = float(self.base_salary_var.get())
        except ValueError:
            return messagebox.showerror("Ошибка", "Неверное значение базовой зарплаты")
        emp_type = self.emp_type_var.get()

        if emp_type == "Manager":
            try:
                bonus = float(self.bonus_var.get())
            except ValueError:
                return messagebox.showerror("Ошибка", "Неверное значение бонуса")
            emp = Manager(name, base, bonus)

        else:
            try:
                oh = float(self.overtime_hours_var.get())
                orate = float(self.overtime_rate_var.get())
            except ValueError:
                return messagebox.showerror("Ошибка", "Неверные параметры сверхурочных")
            emp = Engineer(name, base, oh, orate)

        self.company.add_employee(emp)
        self.emp_listbox.insert("end", str(emp))
        # Сброс полей
        for var in (self.name_var, self.base_salary_var,
                    self.bonus_var, self.overtime_hours_var,
                    self.overtime_rate_var):
            var.set("")

    def _remove_selected(self):
        sel = self.emp_listbox.curselection()
        if not sel:
            return messagebox.showwarning("Внимание", "Ничего не выбрано")
        idx = sel[0]
        self.company.remove_employee(idx)
        self.emp_listbox.delete(idx)

    def _show_payroll(self):
        payroll = self.company.calculate_payroll()
        self.payroll_text.delete("1.0", "end")
        for emp, amt in payroll.items():
            self.payroll_text.insert("end",
                f"{emp.name} ({emp.position}): {amt:,.0f}₸\n"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()
