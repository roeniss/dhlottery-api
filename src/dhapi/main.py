from dhapi.router.router import entrypoint


def main():
    entrypoint()


if __name__ == "__main__":
    import sys
    sys.argv = ["dhapi","show-balance",]  # 명령어 인수를 하드코딩
    entrypoint()
