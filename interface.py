import subprocess

if __name__ == '__main__':
    while True:
        inp = input('Input: ')

        out = subprocess.check_output(
            args=['./main'],
            input=inp,
            text=True
        )

        print(f'Output: {out}')