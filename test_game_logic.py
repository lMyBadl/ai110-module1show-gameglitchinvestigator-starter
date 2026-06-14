import pytest
from app import get_range_for_difficulty, parse_guess, check_guess, update_score


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_returns_1_to_20(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_returns_1_to_100(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard_returns_1_to_50(self):
        assert get_range_for_difficulty("Hard") == (1, 50)

    def test_unknown_difficulty_defaults_to_1_to_100(self):
        assert get_range_for_difficulty("Extreme") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    # --- empty / missing input ---

    def test_none_input_is_rejected(self):
        ok, val, err = parse_guess(None)
        assert not ok
        assert val is None
        assert err is not None

    def test_empty_string_is_rejected(self):
        ok, val, err = parse_guess("")
        assert not ok
        assert val is None
        assert err is not None

    # --- non-numeric input ---

    def test_letters_are_rejected(self):
        ok, val, err = parse_guess("abc")
        assert not ok
        assert val is None
        assert "not a number" in err.lower()

    def test_special_chars_are_rejected(self):
        ok, val, err = parse_guess("!@#")
        assert not ok

    # --- valid numeric input ---

    def test_valid_integer_is_accepted(self):
        ok, val, err = parse_guess("50")
        assert ok
        assert val == 50
        assert err is None

    def test_decimal_is_truncated_to_int(self):
        ok, val, err = parse_guess("7.9")
        assert ok
        assert val == 7
        assert err is None

    def test_decimal_at_boundary_is_accepted(self):
        ok, val, err = parse_guess("1.0", 1, 100)
        assert ok
        assert val == 1

    # --- range validation (defaults 1-100) ---

    def test_lower_boundary_is_accepted(self):
        ok, val, err = parse_guess("1", 1, 100)
        assert ok
        assert val == 1

    def test_upper_boundary_is_accepted(self):
        ok, val, err = parse_guess("100", 1, 100)
        assert ok
        assert val == 100

    def test_below_range_is_rejected(self):
        ok, val, err = parse_guess("0", 1, 100)
        assert not ok
        assert val is None
        assert err is not None

    def test_above_range_is_rejected(self):
        ok, val, err = parse_guess("101", 1, 100)
        assert not ok
        assert val is None
        assert err is not None

    # --- range validation respects difficulty ranges ---

    def test_easy_mode_rejects_above_20(self):
        ok, val, err = parse_guess("21", 1, 20)
        assert not ok
        assert "20" in err

    def test_easy_mode_accepts_20(self):
        ok, val, err = parse_guess("20", 1, 20)
        assert ok

    def test_hard_mode_rejects_above_50(self):
        ok, val, err = parse_guess("51", 1, 50)
        assert not ok
        assert "50" in err

    def test_hard_mode_accepts_50(self):
        ok, val, err = parse_guess("50", 1, 50)
        assert ok

    def test_error_message_includes_range_bounds(self):
        ok, val, err = parse_guess("200", 1, 100)
        assert not ok
        assert "1" in err and "100" in err


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_correct_guess_wins(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_correct_guess_win_message(self):
        _, message = check_guess(42, 42)
        assert "correct" in message.lower() or "🎉" in message

    def test_guess_higher_than_secret_is_too_high(self):
        outcome, _ = check_guess(80, 50)
        assert outcome == "Too High"

    def test_guess_lower_than_secret_is_too_low(self):
        outcome, _ = check_guess(20, 50)
        assert outcome == "Too Low"

    def test_too_high_hint_tells_player_to_go_lower(self):
        _, message = check_guess(80, 50)
        assert "lower" in message.lower()

    def test_too_low_hint_tells_player_to_go_higher(self):
        _, message = check_guess(20, 50)
        assert "higher" in message.lower()

    def test_boundary_one_above_secret_is_too_high(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_boundary_one_below_secret_is_too_low(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    # --- Win outcomes ---

    def test_win_on_first_attempt_gives_max_points(self):
        # attempt 0: 100 - 10*(0+1) = 90
        assert update_score(0, "Win", 0) == 90

    def test_win_later_gives_fewer_points(self):
        early = update_score(0, "Win", 1)
        late = update_score(0, "Win", 5)
        assert late < early

    def test_win_score_is_floored_at_10(self):
        # attempt 9: 100 - 10*10 = 0 → clamped to 10
        assert update_score(0, "Win", 9) == 10

    def test_win_score_below_floor_still_gives_10(self):
        # attempt 15: 100 - 10*16 = -60 → clamped to 10
        assert update_score(0, "Win", 15) == 10

    def test_win_adds_to_existing_score(self):
        assert update_score(50, "Win", 0) == 140  # 50 + 90

    # --- Too High outcomes ---

    def test_too_high_on_even_attempt_adds_5(self):
        assert update_score(50, "Too High", 2) == 55

    def test_too_high_on_odd_attempt_subtracts_5(self):
        assert update_score(50, "Too High", 1) == 45

    # --- Too Low outcomes ---

    def test_too_low_always_subtracts_5(self):
        assert update_score(50, "Too Low", 1) == 45

    def test_too_low_on_even_attempt_still_subtracts_5(self):
        assert update_score(50, "Too Low", 2) == 45

    # --- Unknown outcome ---

    def test_unknown_outcome_leaves_score_unchanged(self):
        assert update_score(50, "SomethingElse", 1) == 50

    # --- Score accumulation across a game ---

    def test_score_accumulates_across_multiple_guesses(self):
        score = 0
        score = update_score(score, "Too Low", 1)   # -5 → -5
        score = update_score(score, "Too High", 2)  # +5 →  0
        score = update_score(score, "Win", 3)       # 100-40=60 → 60
        assert score == 60


# ---------------------------------------------------------------------------
# Multi-guess sequences — check_guess
# ---------------------------------------------------------------------------

class TestCheckGuessSequence:
    """Each test simulates a player making several guesses in a row."""

    def test_binary_search_converges_to_win(self):
        secret = 50
        # 1st guess: below midpoint
        outcome, msg = check_guess(25, secret)
        assert outcome == "Too Low"
        assert "higher" in msg.lower()
        # 2nd guess: above midpoint
        outcome, msg = check_guess(75, secret)
        assert outcome == "Too High"
        assert "lower" in msg.lower()
        # 3rd guess: exact
        outcome, _ = check_guess(50, secret)
        assert outcome == "Win"

    def test_high_to_low_sequence_ends_in_win(self):
        secret = 30
        guesses = [100, 50, 25, 30]
        expected_outcomes = ["Too High", "Too High", "Too Low", "Win"]
        for guess, expected in zip(guesses, expected_outcomes):
            outcome, _ = check_guess(guess, secret)
            assert outcome == expected, f"guess={guess}: expected {expected}, got {outcome}"

    def test_all_guesses_below_secret_are_too_low(self):
        secret = 80
        for guess in [1, 10, 30, 50, 79]:
            outcome, _ = check_guess(guess, secret)
            assert outcome == "Too Low", f"guess={guess} should be Too Low"

    def test_all_guesses_above_secret_are_too_high(self):
        secret = 20
        for guess in [21, 40, 60, 80, 100]:
            outcome, _ = check_guess(guess, secret)
            assert outcome == "Too High", f"guess={guess} should be Too High"

    def test_hint_directions_are_consistent_across_many_guesses(self):
        secret = 50
        low_guesses = [1, 10, 25, 49]
        high_guesses = [51, 60, 75, 100]
        for guess in low_guesses:
            _, msg = check_guess(guess, secret)
            assert "higher" in msg.lower(), f"guess={guess} is too low — hint should say higher"
        for guess in high_guesses:
            _, msg = check_guess(guess, secret)
            assert "lower" in msg.lower(), f"guess={guess} is too high — hint should say lower"

    def test_multiple_wrong_guesses_before_win(self):
        secret = 42
        wrong_guesses = [10, 80, 30, 60, 42]
        outcomes = []
        for g in wrong_guesses:
            outcome, _ = check_guess(g, secret)
            outcomes.append(outcome)
        assert outcomes[-1] == "Win"
        assert all(o != "Win" for o in outcomes[:-1])


# ---------------------------------------------------------------------------
# Multi-guess sequences — update_score
# ---------------------------------------------------------------------------

class TestUpdateScoreSequence:
    """Each test simulates a full game's worth of score updates."""

    def test_all_too_low_then_win(self):
        # Attempts 1-4 all Too Low (-5 each), win at attempt 5.
        # Win at attempt 5: 100 - 10*(5+1) = 40 points.
        # Expected final score: 0 - 5 - 5 - 5 - 5 + 40 = 20
        score = 0
        for attempt in range(1, 5):
            score = update_score(score, "Too Low", attempt)
        score = update_score(score, "Win", 5)
        assert score == 20

    def test_alternating_too_high_too_low_then_win(self):
        # Attempt 1: Too Low → -5 (score: -5)
        # Attempt 2: Too High even → +5 (score: 0)
        # Attempt 3: Too Low → -5 (score: -5)
        # Attempt 4: Too High even → +5 (score: 0)
        # Attempt 5: Win → 100 - 60 = 40 (score: 40)
        score = 0
        score = update_score(score, "Too Low", 1)
        score = update_score(score, "Too High", 2)
        score = update_score(score, "Too Low", 3)
        score = update_score(score, "Too High", 4)
        score = update_score(score, "Win", 5)
        assert score == 40

    def test_winning_on_last_allowed_attempt_gives_minimum_win_points(self):
        # Eight failed guesses (attempt limit for Normal is 8), win at attempt 9.
        # Win at attempt 9: 100 - 10*10 = 0 → clamped to 10.
        score = 0
        for attempt in range(1, 9):
            score = update_score(score, "Too Low", attempt)
        score = update_score(score, "Win", 9)
        expected = (0 - 5 * 8) + 10   # -40 + 10 = -30
        assert score == expected

    def test_too_high_even_attempts_all_add_points(self):
        # Attempts 2, 4, 6 are all even Too High → each adds 5
        score = 0
        for attempt in [2, 4, 6]:
            score = update_score(score, "Too High", attempt)
        assert score == 15

    def test_too_high_odd_attempts_all_subtract_points(self):
        # Attempts 1, 3, 5 are all odd Too High → each subtracts 5
        score = 50
        for attempt in [1, 3, 5]:
            score = update_score(score, "Too High", attempt)
        assert score == 35

    def test_losing_game_only_accrues_penalties(self):
        # A game where every guess is Too Low — score just drops by 5 each time
        score = 0
        for attempt in range(1, 9):
            score = update_score(score, "Too Low", attempt)
        assert score == -40


# ---------------------------------------------------------------------------
# Multi-guess sequences — parse_guess
# ---------------------------------------------------------------------------

class TestParseGuessSequence:
    """Each test submits a stream of inputs, mixing valid and invalid entries."""

    def test_invalid_inputs_followed_by_valid_one(self):
        bad_inputs = [None, "", "xyz", "0", "101"]
        for raw in bad_inputs:
            ok, val, _ = parse_guess(raw, 1, 100)
            assert not ok, f"'{raw}' should be rejected"
        # Finally a valid guess
        ok, val, _ = parse_guess("50", 1, 100)
        assert ok
        assert val == 50

    def test_same_number_across_three_difficulties(self):
        # 15 is valid in all three difficulty ranges
        for difficulty in ["Easy", "Normal", "Hard"]:
            low, high = get_range_for_difficulty(difficulty)
            ok, val, _ = parse_guess("15", low, high)
            assert ok, f"15 should be valid for {difficulty} (range {low}-{high})"
            assert val == 15

    def test_boundary_numbers_accepted_then_exceeded(self):
        low, high = 1, 20  # Easy
        ok, _, _ = parse_guess("1", low, high)
        assert ok
        ok, _, _ = parse_guess("20", low, high)
        assert ok
        ok, _, _ = parse_guess("21", low, high)
        assert not ok

    def test_mix_of_decimals_and_integers_in_sequence(self):
        inputs_and_expected = [
            ("5.0", 5),
            ("10",  10),
            ("7.9", 7),
            ("20",  20),
        ]
        for raw, expected_val in inputs_and_expected:
            ok, val, _ = parse_guess(raw, 1, 100)
            assert ok, f"'{raw}' should be accepted"
            assert val == expected_val, f"'{raw}' should parse to {expected_val}, got {val}"


# ---------------------------------------------------------------------------
# End-to-end game simulations
# ---------------------------------------------------------------------------

class TestFullGameSimulation:
    """
    Simulates a complete game by running parse_guess → check_guess → update_score
    for each guess, the same way the app does it.
    """

    def test_three_guess_win_correct_final_score(self):
        # Secret = 50, Normal difficulty (1-100)
        secret, low, high = 50, 1, 100
        score = 0

        # Attempt 1: "25" → Too Low → score -5
        ok, guess, _ = parse_guess("25", low, high)
        assert ok
        outcome, msg = check_guess(guess, secret)
        assert outcome == "Too Low"
        assert "higher" in msg.lower()
        score = update_score(score, outcome, 1)
        assert score == -5

        # Attempt 2: "75" → Too High → score 0  (even attempt: +5)
        ok, guess, _ = parse_guess("75", low, high)
        assert ok
        outcome, msg = check_guess(guess, secret)
        assert outcome == "Too High"
        assert "lower" in msg.lower()
        score = update_score(score, outcome, 2)
        assert score == 0

        # Attempt 3: "50" → Win → score 60  (100 - 10*(3+1) = 60)
        ok, guess, _ = parse_guess("50", low, high)
        assert ok
        outcome, _ = check_guess(guess, secret)
        assert outcome == "Win"
        score = update_score(score, outcome, 3)
        assert score == 60

    def test_invalid_guesses_do_not_advance_game_state(self):
        # Invalid inputs should parse-fail; game outcome and score stay unchanged
        secret, low, high = 42, 1, 100
        score = 0

        for bad in ["", "abc", "0", "101"]:
            ok, _, _ = parse_guess(bad, low, high)
            assert not ok
            # score and game state are unchanged — nothing to pass to check_guess

        # Only a valid guess advances the game
        ok, guess, _ = parse_guess("42", low, high)
        assert ok
        outcome, _ = check_guess(guess, secret)
        assert outcome == "Win"
        score = update_score(score, outcome, 1)
        assert score == 80   # 100 - 10*(1+1) = 80

    def test_easy_mode_full_game_respects_range(self):
        # Easy: range 1-20, 6 attempts allowed
        secret, low, high = 10, 1, 20
        score = 0

        # Out-of-range guesses are rejected before reaching check_guess
        ok, _, _ = parse_guess("21", low, high)
        assert not ok

        # Attempt 1: "5" → Too Low
        ok, guess, _ = parse_guess("5", low, high)
        assert ok
        outcome, msg = check_guess(guess, secret)
        assert outcome == "Too Low"
        assert "higher" in msg.lower()
        score = update_score(score, outcome, 1)

        # Attempt 2: "15" → Too High
        ok, guess, _ = parse_guess("15", low, high)
        assert ok
        outcome, msg = check_guess(guess, secret)
        assert outcome == "Too High"
        assert "lower" in msg.lower()
        score = update_score(score, outcome, 2)

        # Attempt 3: "10" → Win
        ok, guess, _ = parse_guess("10", low, high)
        assert ok
        outcome, _ = check_guess(guess, secret)
        assert outcome == "Win"
        score = update_score(score, outcome, 3)
        # Too Low (-5) + Too High even (+5) + Win at attempt 3 (100-40=60) = 60
        assert score == 60
