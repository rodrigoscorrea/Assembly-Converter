.code 
  add r0,r1
  shr r0,r1
  shl r0,r1
  not r0,r1
  data r0,15
  data r3,0x05
  and r0,r1
  or r0,r1
  xor r0,r1
  cmp r0,r1
  ld r0,r1
  st r0,r1
  jmpr r3
  jmp 0x20
  ja 0x13
  clf
  in data,r1 
  in addr, r2
  out data, r3
  out addr, r0
  move r1, r0
  halt
.data 
  word 10
  word 0x15
