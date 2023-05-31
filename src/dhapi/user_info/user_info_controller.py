from dhapi.client.lottery_client import LotteryClient


# TODO: 유저의 정보를 확인하는 모듈로 활용할 예정
class UserInfo:
    def __init__(self):
        self.client = LotteryClient()
