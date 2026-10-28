from noirwrit.train.plan_run import MAX_EPOCHS, choose, make_plan

TPS = 65_536


def test_flops_formula():
    p = make_plan("small", 1_000_000_000, 50_000, 0.5, TPS, "estimate")
    assert abs(p.flops - 6 * p.params * p.tokens) < 1
    assert abs(p.hours - p.tokens / 50_000 / 3600) < 0.01
    assert abs(p.usd - p.hours * 0.5) < 0.01


def test_free_gpu_picks_base_up_to_four_epochs():
    plan = choose(100_000_000, {"base": 25_000, "small": 70_000}, usd_hr=0, budget_usd=0, max_hours=22,
                  tokens_per_step=TPS, source="estimate")
    assert plan.preset == "base"
    assert plan.tokens <= 100_000_000 * MAX_EPOCHS
    assert plan.hours <= 22


def test_budget_cuts_epochs_then_drops_to_small():
    # $8 at $0.45/hr gives 16 h; base at a slow 1500 tok/s cannot do one epoch of 100M tokens.
    plan = choose(100_000_000, {"base": 1_500, "small": 6_000}, usd_hr=0.45, budget_usd=8, max_hours=48,
                  tokens_per_step=TPS, source="probe")
    assert plan.preset == "small"
    assert plan.usd <= 8


def test_budget_respected_with_margin():
    plan = choose(300_000_000, {"base": 60_000, "small": 150_000}, usd_hr=0.45, budget_usd=8, max_hours=48,
                  tokens_per_step=TPS, source="probe")
    assert plan.usd <= 8 * 0.9 + 0.01
