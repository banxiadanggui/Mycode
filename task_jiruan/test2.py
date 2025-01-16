def main():
    test = [24, 30, 23, 41, 51, 68, 46, 11, 14, 61, 35]
    hash1 = [0] * 15
    hash2 = [0] * 13
    success1 = success2 = fail1 = fail2 = 0

    for i in range(11):  # 实验1
        h = test[i] % 13
        for j in range(15):
            success1 += 1
            if hash1[h] == 0:
                hash1[h] = test[i]
                break
            else:
                h = (h + 1) % 15

    for i in range(15):
        t = i
        while True:
            fail1 += 1
            if hash1[t] == 0:
                break
            else:
                t = (t + 1) % 15

    print(' '.join(map(str, hash1)))
    print("successful asl: {:.6f}".format(success1 / 11.0))
    print("failed asl: {:.6f}".format(fail1 / 13.0))

    for i in range(11):  # 实验2
        h = test[i] % 13
        for j in range(13):
            success2 += 1
            if hash2[h] == 0:
                hash2[h] = test[i]
                break
            else:
                h = (h + 1) % 13

    for i in range(13):
        t = i
        while True:
            fail2 += 1
            if hash2[t] == 0:
                break
            else:
                t = (t + 1) % 13

    print('\n' + ' '.join(map(str, hash2)))
    print("successful asl: {:.6f}".format(success2 / 11.0))
    print("failed asl: {:.6f}".format(fail2 / 13.0))

if __name__ == "__main__":
    main()