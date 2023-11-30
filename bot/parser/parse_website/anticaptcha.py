from anticaptchaofficial.imagecaptcha import *

from .exceptions import NotEnoughMoneyException

API_KEY = "178480a4f2942503ca93d0836d11f2cb"


def solve_captcha(captcha_src: str) -> str:
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(API_KEY)

    # Specify softId to earn 10% commission with your app.
    # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
    solver.set_soft_id(0)

    balance = solver.get_balance()
    print(balance)
    if balance <= 0:
        balance = solver.get_balance()
        if balance <= 0:
            raise NotEnoughMoneyException('Пополните баланс антикапчи на https://anti-captcha.com/')

    captcha_text = solver.solve_and_return_solution(captcha_src)
    if captcha_text != 0:
        return captcha_text
    else:
        print("task finished with error " + solver.error_code)


if __name__ == '__main__':
    print(PageParser().parse('66:41:0206030:2313'))
