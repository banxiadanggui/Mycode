def main():
    test = [46, 25, 40, 15, 67, 34, 6, 21]
    hash1 = [0] * 11
    hash2 = [0] * 11
    success1 = success2 = fail1 = fail2 = 0

    for i in range(8):  # 实验1
        h = test[i] % 11
        for j in range(1, 11):
            success1 += 1
            if hash1[h] == 0:
                hash1[h] = test[i]
                break
            else:
                h = (h + 1) % 11

    for i in range(11):
        t = i
        while True:
            fail1 += 1
            if hash1[t] == 0:
                break
            else:
                t = (t + 1) % 11

    print(' '.join(map(str, hash1)))
    print("successful asl: {:.6f}".format(success1 / 8.0))
    print("failed asl: {:.6f}".format(fail1 / 11.0))
    print()

    for i in range(8):  # 实验2
        h = k = test[i] % 11
        for j in range(1, 11):
            success2 += 1
            if hash2[h] == 0:
                hash2[h] = test[i]
                break
            else:
                if j % 2 == 1:
                    h = (k + (j // 2 + 1) ** 2) % 11
                else:
                    h = (k - (j // 2) ** 2) % 11

    for i in range(11):
        t = i
        j = 1
        while True:
            fail2 += 1
            if hash2[t] == 0:
                break
            else:
                if j % 2 == 1:
                    t = (i + (j // 2 + 1) ** 2) % 11
                else:
                    t = (i - (j // 2) ** 2) % 11
                j += 1

    print(' '.join(map(str, hash2)))
    print("successful asl: {:.6f}".format(success2 / 8.0))
    print("failed asl: {:.6f}".format(fail2 / 11.0))

if __name__ == "__main__":
    main()