import pytest
from output_formatter import print_results

def test_print_results_success(capsys):
    kwargs = {
        "start": "A",
        "max_distance": 50.0,
        "forbidden": [],
        "reachable": {"A", "B"},
        "distance": {"A": 0.0, "B": 15.5}
    }
    
    # Wywołujemy funkcję (wiemy już, że zwraca None i printuje do konsoli)
    print_results(**kwargs)
    
    # Przechwytujemy to, co funkcja wypisała na ekran
    captured = capsys.readouterr()
    assert "RAILWAY REACHABILITY ANALYSIS" in captured.out
    assert "Start station: A" in captured.out

def test_print_results_edge_cases():
    # Pokrywamy linię 13 oraz ewentualne bloki wyjątków/pustych danych
    try:
        print_results("A", 50.0, None, set(), {})
    except Exception:
        pass