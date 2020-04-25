from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from djangotoolbox.fields import EmbeddedModelField, ListField

from ikwen.core.models import Model
from ikwen.accesscontrol.models import Member


class Session(Model):
    IMG_BASE_FOLDER = 'sessions/'
    
    RACE = 1
    FOOT = 2
    
    PENDING = 1
    RUNNING = 2
    TERMINATED = 3
    CLOSED = 4

    COMPANY_SHARE = 0.4  # 40 % of the total revenue
    GOLD_SHARE = 0.6  # 60 % after the company share has been removed
    SILVER_SHARE = 0.28  # 28 %
    BRONZE_SHARE = 0.12  # 12 %
    
    title = models.CharField(max_length=150)
    # image = models.Im(max_length=150)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    winning_combination = models.CharField(max_length=150)
    
    def get_truncated_winning_combination_for(self, bet_type):
        if bet_type == Bet.QUINTE or bet_type == Bet.TROIS_SUR_5:
            length = 5
        elif bet_type == Bet.QUARTE or bet_type == Bet.DEUX_SUR_4:
            length = 4
        elif bet_type == Bet.TIERCE or bet_type == Bet.COUPLE:
            length = 3
        tokens = self.winning_combination.split('.')
        return '.'.join(tokens[:length])


class Bet(Model):        
    QUINTE = 5
    QUARTE = 4
    TIERCE = 3
    TROIS_SUR_5 = 35
    COUPLE = 23
    DEUX_SUR_4 = 2
    EOF = 1  # Even/Odd Football
    EOR = 1  # Even/Odd Race

    ORDER = 'Order'
    DISORDER = 'Disorder'
    BONUS = 'Bonus'
    
    COUPLE_A = 'Couple A'
    COUPLE_B = 'Couple B'
    COUPLE_C = 'Couple C'
    
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"
    
    EO = 10
    SIMPLE_SPORT = 11
    
    LOST = 'Lost'

    session = models.ForeignKey(Session)
    type = models.CharField(max_length=30)
    combination = models.CharField(max_length=30)
    gain = models.CharField(max_length=30)

    def __compute_eo_gain(self):
        winning_combination = self.session.winning_combination.split('.')
        combination = self.combination.split('.')
        tokens_count = len(winning_combination)
        if len(combination) != tokens_count:
            return Bet.LOST
        found = 0
        for couple in zip(combination, winning_combination):
            if couple[0] == couple[1]:
                found += 1
        gain = Bet.LOST
        if found == tokens_count:
            gain = Bet.GOLD
        elif found == (tokens_count - 1):
            gain = Bet.SILVER
        elif found == (tokens_count - 2):
            gain = Bet.BRONZE
        return gain

    def compute_gain(self):
        if not self.session.winning_combination or self.gain != None:
            return
        if self.type == Bet.EOF or  self.type == Bet.EOR:
            gain = self.__compute_eo_gain()
        elif self.type == Bet.COUPLE:
            gain = self.__compute_couple_gain()
        else:
            gain = self.__compute_classic_PMU_gain()

        if not self.gain:
            self.gain = gain
            self.save()

    def __compute_classic_PMU_gain(self):
        gain = Bet.LOST
        truncated_winning_combination = self.session.get_truncated_winning_combination_for(self.type)
        if self.combination == truncated_winning_combination:
            gain = Bet.ORDER
        else:
            winning_combination = truncated_winning_combination.split('.')
            combination = self.combination.split('.')
            tokens_count = len(winning_combination)
            found = 0
            for token in combination:
                if token in winning_combination:
                    found += 1
            if found == tokens_count:
                gain = Bet.DISORDER
            if self.type == Bet.QUINTE:
                if found == (tokens_count - 1):
                    gain = Bet.BONUS
            if self.type == Bet.TROIS_SUR_5:
                if found >= 3:
                    gain = Bet.ORDER
            if self.type == Bet.DEUX_SUR_4:
                if found >= 2:
                    gain = Bet.ORDER
        return gain

    def __compute_couple_gain(self):
        truncated_winning_combination = self.session.get_truncated_winning_combination_for(self.type)
        winning_combination = truncated_winning_combination.split('.')
        combination = self.combination.split('.')
        tokens_count = len(winning_combination)
        found = 0
        # First look for couple A, only the first two of winning combination
        # are taken into consideration
        for token in combination[:2]:
            if token in winning_combination:
                found += 1
        if found == 2:
            return Bet.COUPLE_A
        # Next look for couple B, all 3 are taken into consideration
        haystack = winning_combination
        # Couple B is searched between the first and third horses of the
        # combination, so I replace the second horse by an arbitrary value
        # that never exists that is X. match to this 0 will always return false
        haystack[1] = 'X'
        for token in combination[:3]:
            if token in haystack:
                found += 1
        if found == 2:
            return Bet.COUPLE_B

        # Next look for couple B, all 3 are taken into consideration
        haystack = winning_combination
        # Couple C is searched between the second and third horses of the
        # combination, so I replace the first horse by an arbitrary value
        # that never exists that is 0. match to this 0 will always return false
        haystack[0] = 'X'
        for token in combination[:3]:
            if token in haystack:
                found += 1
        if found == 2:
            return Bet.COUPLE_C
        return Bet.LOST
    
    def get_cost(self, type):
        return 100


class Ticket(Model):
    member = models.ForeignKey(Member)
    bet_list = ListField(EmbeddedModelField('Bet'))
    cost = models.IntegerField()

    def get_obj_details(self):
        return "%d comb. %s F" % (len(self.bet_list), intcomma(self.cost))

