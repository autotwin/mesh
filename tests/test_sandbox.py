import atmesh.sandbox as sb


def test_no_decorator():
    # assert 4 == 1
    assert 1 == 1


@sb.run_only_on_cubit_machines
def test_decorator():
    # assert 4 == 1
    assert 1 == 1
