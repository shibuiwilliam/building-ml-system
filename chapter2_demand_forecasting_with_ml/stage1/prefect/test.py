from prefect import task, Flow, Parameter
from prefect.tasks.control_flow.case import case
from prefect.run_configs import LocalRun


@task
def a_or_b_or_c(num):
    i = num % 3
    return ["a", "b", "c"][i]


@task
def proc_a1():
    print("processing a1")
    return "a1"


@task
def proc_a2():
    print("processing a2")
    return "a2"


@task
def proc_b():
    print("processing b")
    return "b"


@task
def proc_c():
    print("processing c")
    return "c"


@task
def cleanup(res):
    print(f"cleanup {res}")


with Flow("test") as flow:
    flow.run_config = LocalRun()

    num = Parameter("num")
    cond = a_or_b_or_c(num)

    with case(cond, "a"):
        res_a1 = proc_a1()
        res_a2 = proc_a2()
        print_a = cleanup([res_a1, res_a2])
    with case(cond, "b"):
        res_b = proc_b()
        print_b = cleanup(res_b)
    with case(cond, "c"):
        res_c = proc_c()
        print_c = cleanup(res_c)

flow.run(num=6)
