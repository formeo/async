import random
import logging
import asyncio

async def call_to(name):
    cnt = 0
    max_ring = 7
    result = False
    logging.debug("Calling {} ...".format(name))
    attempts = random.randrange(0, 9, 1) + 1

    while cnt < attempts:
        await asyncio.sleep(1.0)
        logging.debug("({}): beep".format(name))
        cnt += 1
        if cnt == max_ring:
            logging.debug("({}): not picked up".format(name))
            break
    else:
        result = True
    return result


async def sell_on(name):
    cnt = 0
    max_offer = 3
    logging.debug("Responding {} ...".format(name))
    while True:
        cnt += 1
        await asyncio.sleep(1.0)
        answer = random.randrange(0, 3, 1)
        if answer == 2:
            logging.debug("({}): Yes, I will come".format(name))
            return True
        elif  answer == 1:
            logging.debug("({}): No, I will not come".format(name))
            return False
        else:
            if cnt == max_offer:
                logging.debug("({}): No, I will not come".format(name))
                return False
            else:
                logging.debug("({}): Maybe, I don't know".format(name))


async def invite(name, result):
    answered = await call_to(name)
    if answered:
        agreed = await sell_on(name)
        result.append((name, agreed))
    else:
        result.append((name, answered))


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    result = list()
    frends = ['Саша', 'Паша', 'Катя', 'Маша', 'Дуся', 'Маруся', 'Ваня']
    tasks = [invite(name, result) for name in frends]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print("\n----------------------------------------")
    for name, agreed in result:
        print("{}\t{}".format(name, "придет" if agreed else "не придет"))

    loop.close()