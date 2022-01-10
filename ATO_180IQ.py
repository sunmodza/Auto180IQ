# -*- coding: utf-8 -*-

from itertools import combinations
from functools import reduce
import numpy as np
import threading
import multiprocessing
import random as rd
import numbers

import tkinter as tk
from time import sleep
import math



class NumberWithText:
    def __init__(self, num, text=None):
        self.num = num
        if text is None:
            self.text = f'{num}'
        else:
            self.text = text

    def __repe__(self):
        return f'{self.text}'

    def __str__(self):
        return f'{self.text}'

    def __add__(self, b):
        return NumberWithText(self.num+b.num, f'({self.text}+{b.text})')

    def __mul__(self, b):
        return NumberWithText(self.num*b.num, f'({self.text}x{b.text})')

    def __sub__(self, b):
        return NumberWithText(self.num-b.num, f'({self.text}-{b.text})')

    def __truediv__(self, b):
        return NumberWithText(self.num/b.num, f'({self.text}/{b.text})')

    def __pow__(self, b):
        return NumberWithText(self.num**b.num, f'({self.text}^{b.text})')

    def factorial(self):
        return NumberWithText(math.factorial(self.num), f'({self.text}!)')


def double_plus_combi(N, max_n=4):
    ans = []
    if N == 0:
        return 0
    return ans


def anything_is_closet(quest, ans, g):
    sortv = []
    for i in quest:
        dist_phd = abs(i.num-ans.num)
        sortv.append(SortObj(i, i, dist_phd))
    p = sorted(sortv)
    g = 0
    if p[g].subset is None:
        return None, p[g].value
    return [p[g].subset], p[g].value


def factorial(N):
    if N > 10 or isinstance(N, numbers.Integral):
        return None
    if N.num == 1:
        return NumberWithText(1)
    return N*factorial(N-NumberWithText(1))


def anything_factorial_closet(quest, ans, g):
    sortv = []
    for i in quest:
        if i.num > 7 or i.num < 0 or not isinstance(i.num, numbers.Integral) or i.num == 1 or i.num == 2:
            continue
        abc = i.factorial()
        if abc is None:
            continue
        dist_phd = abs(abc.num-ans.num)
        sortv.append(SortObj(abc, i, dist_phd))
    p = sorted(sortv)
    g = 0
    if len(p) == 0:
        return None, None
    if p[g].subset is None:
        return None, None
    return [p[g].subset], p[g].value


def anything_plus_closet(quest, ans, g):
    sortv = []
    for i in range(2, len(quest)+1):
        combi = combinations(quest, i)
        for subset in combi:
            vas = reduce(lambda x, y: x+y, subset)
            dist_phd = abs(ans.num - vas.num)
            sortv.append(SortObj(vas, subset, dist_phd))
    p = sorted(sortv)
    try:
        g = rd.randint(0, len(p)-1)
    except:
        g = 0
    if p[g].subset is None:
        return None, p[g].value
    return [*(p[g].subset)], p[g].value


def anything_mul_closet(quest, ans, g):
    sortv = []
    for i in range(2, len(quest)+1):
        combi = combinations(quest, i)
        for subset in combi:
            vas = reduce(lambda x, y: x*y, subset)
            dist_phd = abs(ans.num - vas.num)
            sortv.append(SortObj(vas, subset, dist_phd))
    p = sorted(sortv)
    try:
        g = rd.randint(0, len(p)-1)
    except:
        g = 0
    if p[g].subset is None:
        return None, p[g].value
    return [*(p[g].subset)], p[g].value


def special_exp(subset):
    ans = subset[0]
    for i in subset[1:]:
        if abs(i.num) == 0 or abs(ans.num) > 20 or abs(i.num) > 10 or (ans.num == 0 and i.num <= 0):
            return None
        ans = ans**i
        if isinstance(ans.num, complex):
            return None
    return ans


def anything_exp_closet(quest, ans, g):
    sortv = []
    for i in range(2, len(quest)+1):
        combi = combinations(quest, i)
        for subset in combi:
            vas = special_exp(subset)
            if vas is None:
                continue
            dist_phd = abs(ans.num - vas.num)
            sortv.append(SortObj(vas, subset, dist_phd))
    p = sorted(sortv)
    try:
        g = rd.randint(0, len(p)-1)
    except:
        g = 0
    if len(p) == 0:
        return None, None
    return [*(p[g].subset)], p[g].value


def anything_minus_closet(quest, ans, g):
    sortv = []
    for i in range(2, len(quest)+1):
        combi = combinations(quest, i)
        for subset in combi:
            vas = reduce(lambda x, y: x-y, subset)
            dist_phd = abs(ans.num - vas.num)
            dist_phd = abs(ans.num - vas.num)
            sortv.append(SortObj(vas, subset, dist_phd))
    p = sorted(sortv)
    try:
        g = rd.randint(0, len(p)-1)
    except:
        g = 0
    if p[g].subset is None:
        return None, p[g].value
    return [*(p[g].subset)], p[g].value


def special_div(subset):
    ans = subset[0]
    for i in subset[1:]:
        if i.num == 0:
            return None
        ans = ans/i
    return ans


class SortObj:
    def __init__(self, value, subset, dis):
        self.value = value
        self.dis = dis
        self.subset = subset

    def __lt__(self, other):
        return self.dis < other.dis

    def __eq__(self, other):
        return self.dis == other.dis


def anything_div_closet(quest, ans, g):
    sortv = []
    for i in range(2, len(quest)+1):
        combi = combinations(quest, i)
        for subset in combi:
            vas = special_div(subset)
            if vas is None:
                continue
            dist_phd = abs(ans.num - vas.num)
            sortv.append(SortObj(vas, subset, dist_phd))
    p = sorted(sortv)
    try:
        g = rd.randint(0, len(p)-1)
    except:
        g = 0
    if len(p) == 0:
        return None, None
    return [*(p[g].subset)], p[g].value


def solution(quest, ans, sol_nums=1, allow_plus=True, allow_minus=True, allow_mul=True, allow_div=True, allow_exp=True, allow_fac=True,TkTextBox = None):
    quest = [NumberWithText(i) for i in quest]
    ans = NumberWithText(ans)
    allow_arg = [allow_plus, allow_minus,
                 allow_mul, allow_div, allow_exp, allow_fac]
    all_methods = [anything_plus_closet, anything_mul_closet, anything_minus_closet,
                   anything_div_closet, anything_exp_closet, anything_factorial_closet]
    methods = [anything_is_closet]
    print(allow_arg)
    for i in range(len(allow_arg)):
        if allow_arg[i] is True or allow_arg[i] == 1:
            methods.append(all_methods[i])
    print(methods)
    packing = [quest]
    worked_text = []
    wpe = 0
    worked = []
    for i in range(500):
        for quest in packing:
            ms = rd.sample(methods, len(methods))
            for m in ms:
                used, equal_to = m(quest, ans, 0)
                wpe += 1
                if used is None:
                    continue
                remain = list(set(quest)-set(used))
                if len(remain) == 0:
                    # print(equal_to,equal_to.num)
                    if equal_to.num == ans.num:
                        # print("ww")
                        # print(equal_to,equal_to.num)
                        # print(len(worked)+1,equal_to,equal_to.num)
                        if equal_to.text not in worked_text:
                            worked_text.append(equal_to.text)
                            worked.append(equal_to)
                            print(len(worked_text), equal_to, equal_to.num, wpe)
                            if TkTextBox is not None:
                                  TkTextBox.insert(tk.END,f'{len(worked_text)} {equal_to.text} \n')
                            else:
                                  print(len(worked_text), equal_to, equal_to.num, wpe)
                        if sol_nums == len(worked_text):
                            return worked
                        break
                elif equal_to is not None and len(remain) > 0:
                    new_pack = [equal_to, *remain]
                    if new_pack not in packing:
                        packing.append(new_pack)
            packing.append(quest)

class IQ180_Solution:
    def __init__(self):
        self.running = False
        super().__init__()

    def set_start(self,quest, ans, sol_nums=1, allow_plus=True, allow_minus=True, allow_mul=True, allow_div=True, allow_exp=True, allow_fac=True,TkTextBox = None):
        self.quest = [NumberWithText(i) for i in quest]
        self.ans = NumberWithText(ans)
        allow_arg = [allow_plus, allow_minus,
                 allow_mul, allow_div, allow_exp, allow_fac]
        self.sol_nums = sol_nums
        self.allow_plus = allow_plus
        self.allow_minus = allow_minus
        self.allow_mul = allow_mul
        self.allow_div = allow_div
        self.allow_exp = allow_exp
        self.allow_fac = allow_fac
        self.TkTextBox = TkTextBox
        self.packing = [self.quest]
        self.all_methods = [anything_plus_closet, anything_mul_closet, anything_minus_closet,
                   anything_div_closet, anything_exp_closet, anything_factorial_closet]
        self.methods = []
        for i in range(len(allow_arg)):
            if allow_arg[i] is True or allow_arg[i] == 1:
                self.methods.append(self.all_methods[i])
        self.allow_methods_id = range(len(self.methods))
        self.worked_text = []
        self.worked = []
        self.wpe = 0
        self.running = True
        
        #self.solution()
        

    def solution(self):
        while self.running:
            self.run_a_solution()
        while not self.running:
            sleep(0.01)
        self.solution()
    def run_a_solution(self):
        for quest in self.packing:
            #print(quest)
            ms = rd.sample(self.methods, len(self.methods))
            for m in ms:
                used, equal_to = m(quest, self.ans, 0)
                self.wpe += 1
                if used is None:
                    continue
                remain = list(set(quest)-set(used))
                if len(remain) == 0:
                    # print(equal_to,equal_to.num)
                    if equal_to.num == self.ans.num:
                        # print("ww")
                        # print(equal_to,equal_to.num)
                        # print(len(worked)+1,equal_to,equal_to.num)
                        if equal_to.text not in self.worked_text:
                            self.worked_text.append(equal_to.text)
                            self.worked.append(equal_to)
                            print(len(self.worked_text), equal_to, equal_to.num, self.wpe)
                            if self.TkTextBox is not None:
                                  self.TkTextBox.insert(tk.END,f'{len(self.worked_text)} {equal_to.text} \n')
                            else:
                                  print(len(self.worked_text), equal_to, equal_to.num, self.wpe)
                        if self.sol_nums == len(self.worked_text):
                            self.running = False
                            return
                        if not self.running:
                            return 
                    #return
                elif equal_to is not None and len(remain) > 0:
                    new_pack = [equal_to, *remain]
                    if new_pack not in self.packing:
                        self.packing.append(new_pack)
            self.packing.append(quest)

        

def handle_input():
    #solution(question,answer,sol_nums=solnums,allow_plus=plus,allow_minus=minus,allow_mul=mul,allow_div=div,allow_exp=exp,allow_fac=fac,TkTextBox=show_ans)
    #running_threads.terminate()

    #question = [int(i) for i in question_entry.get().split(" ")]
    #answer = int(answer_entry.get())
    #solnums = int(how_many_solutions_entry.get())
    show_ans.delete("1.0", tk.END)
    question = [float(i) for i in question_entry.get().split(" ")]
    answer = float(answer_entry.get())
    solnums = int(how_many_solutions_entry.get())
    obj.set_start(question,answer,sol_nums=solnums,allow_plus=plus.get(),allow_minus=minus.get(),allow_mul=mul.get(),allow_div=div.get(),allow_exp=exp.get(),allow_fac=fac.get(),TkTextBox=show_ans)
    #obj = IQ180_Solution(question,answer,sol_nums=solnums,allow_plus=plus.get(),allow_minus=minus.get(),allow_mul=mul.get(),allow_div=div.get(),allow_exp=exp.get(),allow_fac=fac.get(),TkTextBox=show_ans)

    #global running_threads
    #running_threads.terminate()
    #running_threads.start()

    '''
    try:
      running_threads.terminate()
    except:
      running_threads =multiprocessing.Process(target=doit, args=(1,))
    finally:
      running_threads.start()
    '''
    #running_threads.start()

def doit(a):
    question = [int(i) for i in question_entry.get().split(" ")]
    answer = int(answer_entry.get())
    solnums = int(how_many_solutions_entry.get())
    print(question)
    print(answer)
    print(solnums)
    show_ans.delete("1.0", tk.END)
    solution(question,answer,sol_nums=solnums,allow_plus=plus.get(),allow_minus=minus.get(),allow_mul=mul.get(),allow_div=div.get(),allow_exp=exp.get(),allow_fac=fac.get(),TkTextBox=show_ans)


#quest = [3,2,5,6,1,8]
#ans = 37

#a = solution(quest,ans,sol_nums = 5000)
#running_threads = None
#running_threads = multiprocessing.Process(target=doit, args=())
#question = []
#answer = None
#sol_nums = None

obj = IQ180_Solution()
threading._start_new_thread(obj.solution,())

app = tk.Tk("180iq-solver")
app.title("190iq-noob")

question_text = tk.Label(app, text="your numbers")
question_text.grid(row=0, column=0)

question_entry = tk.Entry(app)
question_entry.grid(row=0, column=1, columnspan=2)

ans_text = tk.Label(app, text="your answer")
ans_text.grid(row=1, column=0)

answer_entry = tk.Entry(app)
answer_entry.grid(row=1, column=1, columnspan=2)

how_many_solutions_text = tk.Label(app, text="solnums")
how_many_solutions_text.grid(row=2, column=0)

how_many_solutions_entry = tk.Entry(app)
how_many_solutions_entry.grid(row=2, column=1, columnspan=2)

find_button = tk.Button(app, text="find it!!",command = handle_input)
find_button.grid(row=5, column=0, columnspan=3)

plus = tk.IntVar()
minus = tk.IntVar()
mul = tk.IntVar()
div = tk.IntVar()
exp = tk.IntVar()
fac = tk.IntVar()

is_plus_allow = tk.Checkbutton(
    app, text="Plus", variable=plus)
is_plus_allow.grid(row=3, column=0)
is_plus_allow.select()
is_minus_allow = tk.Checkbutton(
    app, text="Minus", variable=minus)
is_minus_allow.grid(row=3, column=1)
is_minus_allow.select()
is_mul_allow = tk.Checkbutton(
    app, text="Mul", variable=mul)
is_mul_allow.grid(row=3, column=2)
is_mul_allow.select()
is_div_allow = tk.Checkbutton(
    app, text="Div", variable=div)
is_div_allow.grid(row=4, column=0)
is_div_allow.select()
is_exp_allow = tk.Checkbutton(
    app, text="Exp", variable=exp)
is_exp_allow.grid(row=4, column=1)
is_exp_allow.select()
is_fac_allow = tk.Checkbutton(
    app, text="Fac", variable=fac)
is_fac_allow.grid(row=4, column=2)
is_fac_allow.select()

ans_frame = tk.Frame(app)
ans_frame.grid(row=6, column=0, columnspan=3)

scroller = tk.Scrollbar(ans_frame)
scroller.pack(side=tk.RIGHT, fill=tk.Y)

show_ans = tk.Text(ans_frame, width=30, height=5)
show_ans.pack(side=tk.LEFT)

show_ans.config(yscrollcommand=scroller.set)
scroller.config(command=show_ans.yview)

app.mainloop()
