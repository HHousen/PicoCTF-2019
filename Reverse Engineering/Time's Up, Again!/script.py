import signal
import subprocess
import os
import time
import sys

os.chdir('/problems/time-s-up--again-_1_014490a2cb518921928db099702cbfd9')

num_tries = 0
done = False

while not done:
    print("Iteration #{}".format(num_tries))
    num_tries += 1
    proc = subprocess.Popen('./times-up-again', stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    time.sleep(0.000175)

    proc.send_signal(signal.SIGSTOP)

    challenge = proc.stdout.readline()[10:] # remove first 10 characters (which is the string "Challenge: ")
    
    print("Challenge: " + str(challenge))
    answer = eval(challenge)
    print("Answer: " + str(answer))
    
    # if answer < 0:
    #     proc.kill()
    #     print("Answer less than 0. Restarting...")
    #     continue
    
    try:
        if sys.version_info[0] < 3:
            # don't need to specify 'utf-8' encoding in python 2
            proc.stdin.write(bytes(str(answer%(1 << 64))))
        else:
            proc.stdin.write(bytes(str(answer%(1 << 64)), 'utf-8'))

        # Send an "enter" to submit the answer
        proc.stdin.write(b'\n\n')

        proc.stdin.flush()
    # handle broken pipes (if the program exited before it could be paused)
    except IOError as e:
        print(e)
        continue
    except BrokenPipeError as e:
        print(e)
        continue


    # resume the program
    proc.send_signal(signal.SIGCONT)
    
    # wait for 0.02 seconds to get some input from the program
    time.sleep(0.2)

    proc.stdout.flush()

    for i in range(4):
        line = str(proc.stdout.readline())
        if "pico" in line:
            done = True
            print(line)
            print("It took {} tries to get the flag.".format(num_tries))
