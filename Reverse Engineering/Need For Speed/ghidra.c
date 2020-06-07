undefined8 main(void)

{
  header();
  set_timer();
  get_key();
  print_flag();
  return 0;
}



void header(void)

{
  uint local_c;
  
  puts("Keep this thing over 50 mph!");
  local_c = 0;
  while (local_c < 0x1c) {
    putchar(0x3d);
    local_c = local_c + 1;
  }
  puts("\n");
  return;
}


void set_timer(void)

{
  __sighandler_t p_Var1;
  
  p_Var1 = __sysv_signal(0xe,alarm_handler);
  if (p_Var1 == (__sighandler_t)0xffffffffffffffff) {
    printf(
           "\n\nSomething bad happened here. \nIf running on the shell server\nPlease contact theadmins with \"need-for-speed.c:%d\".\n"
           ,0x3c);
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  alarm(1);
  return;
}


void alarm_handler(void)

{
  puts("Not fast enough. BOOM!");
                    /* WARNING: Subroutine does not return */
  exit(0);
}


void get_key(void)

{
  puts("Creating key...");
  key = calculate_key();
  puts("Finished");
  return;
}


undefined8 calculate_key(void)

{
  int local_c;
  
  local_c = -0x2cc50ef2;
  do {
    local_c = local_c + -1;
  } while (local_c != -0x16628779);
  return 0xe99d7887;
}


void print_flag(void)

{
  puts("Printing flag:");
  decrypt_flag((ulong)key);
  puts(flag);
  return;
}


void decrypt_flag(int param_1)

{
  int local_1c [4];
  uint local_c;
  
  local_1c[0] = param_1;
  local_c = 0;
  while (local_c < 0x37) {
    flag[(int)local_c] =
         flag[(int)local_c] ^
         *(byte *)((long)local_1c +
                  (long)(int)((local_c - ((int)local_c >> 0x1f) & 1) + ((int)local_c >> 0x1f)));
    if ((int)local_c % 3 == 2) {
      local_1c[0] = local_1c[0] + 1;
    }
    local_c = local_c + 1;
  }
  return;
}
