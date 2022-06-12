import pytest
from brownie import accounts, Ballot, convert, reverts

proposals = [1007, 1014, 1021]


@pytest.fixture
def ballot(scope="module"):
    byte_proposals = [convert.to_bytes(p) for p in proposals]
    return Ballot.deploy(byte_proposals, {"from": accounts[0]})


def test_correct_chairperson(ballot):
    assert ballot.chairperson() == accounts[0]


def test_has_proposals(ballot):
    assert convert.to_int(ballot.proposals(0)[0]) == proposals[0]
    assert convert.to_int(ballot.proposals(1)[0]) == proposals[1]
    assert convert.to_int(ballot.proposals(2)[0]) == proposals[2]


def test_rights_to_vote(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    delegate, vote, weight, voted = ballot.voters(accounts[1])
    assert weight == 1


def test_rights_to_vote_nonadmin(ballot):
    with reverts():
        ballot.giveRightToVote(accounts[2], {"from": accounts[1]})
    assert ballot.voters(accounts[2])[2] == 0

def test_rights_to_vote_hasvoted(ballot):
    