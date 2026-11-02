! Native Fortran K06 source-derived R/C solver and native HX89 feedback harness.
! Matrix method: modified nodal G + C/dt, implicit backward Euler; LAPACK DGESV.
! Original .cir/.lib files are read, not redefined as an invented standalone circuit.
module void_rc
 use, intrinsic :: iso_c_binding, only:c_char,c_int,c_int64_t,c_null_char
 use, intrinsic :: iso_fortran_env, only:real64,error_unit
 use, intrinsic :: ieee_arithmetic, only:ieee_is_finite
 implicit none
 private
 integer, parameter :: dp=real64, maxelements=100,maxnodes=80
 character(len=56),parameter :: core(30)=[character(len=56) :: &
 'R_WRITE_A_BLEED','C_WRITE_A_COUPLING','R_WRITE_A_LIMIT', &
 'R_WRITE_B_BLEED','C_WRITE_B_COUPLING','R_WRITE_B_LIMIT', &
 'R_INTEG_A','C_CHARGE_A','R_LEAK_A','R_INTEG_B','C_CHARGE_B','R_LEAK_B', &
 'R_CHARGE_COUPLE','R_FEEDBACK_A','R_FEEDBACK_B','R_INTEG_C','C_CHARGE_C','R_LEAK_C', &
 'R_COUPLE_AC','R_COUPLE_BC','R_FEEDBACK_C','R_MEM_METER_A','R_MEM_METER_B','R_MEM_METER_C', &
 'R_XY_BUFFER_A','R_XY_BUFFER_B','R_XY_BUFFER_C','R_XY_INSTR_A','R_XY_INSTR_B','R_XY_INSTR_C']
 character(len=56),parameter :: mesh(10)=[character(len=56) :: &
 'R_M12','R_MA','R_MB','R_PA','R_PB','C_M12','C_MA','C_MB','C_PA','C_PB']
 character(len=*),parameter :: k06sha='ccfd7ab640ecc54fee5a2414eaca56c920f6c3dd4d1299f1e7f3b61f9c80d161'
 character(len=*),parameter :: meshsha='67cb648471f27c4338ceac014f8569753342fd7b59e4aa0f26cccd7de7db3d15'
 type :: component
  character(56) :: label='',a='',b=''
  character(1) :: kind=' '
  real(dp) :: value=0
 end type
 type(component),save :: elems(maxelements)
 character(len=56),save :: nodes(maxnodes)
 real(dp),save :: conduct(maxnodes,maxnodes),capac(maxnodes,maxnodes),state(maxnodes)
 integer,save :: ne=0,nn=0
 logical,save::skip_a=.false.,skip_b=.false.
 real(dp),save :: olda=0,oldb=0,elapsed=0
 public:: read_circuit,reset_state,solve_step,get_voltage,capacitor_energy,native_decision,cpu_init,cpu_execute,cpu_feedback
 interface
  integer(c_int) function sha_match(filename,expected) bind(c,name='void_sha256_matches')
   import c_char,c_int
   character(kind=c_char),intent(in)::filename(*),expected(*)
  end function
  integer(c_int) function native_eval(exe,a,b,s,bit) bind(c,name='void_hx89_evaluate')
   import c_char,c_int
   character(kind=c_char),intent(in)::exe(*)
   integer(c_int),value::a,b
   integer(c_int),intent(out)::s,bit
  end function
  integer(c_int) function native_cpu_init() bind(c,name='void_cpu_cycle_init')
   import c_int
  end function
  integer(c_int) function native_cpu_work(sel,epoch,digest,ticks,migrated) bind(c,name='void_cpu_cycle_execute')
   import c_int,c_int64_t
   integer(c_int),value::sel,epoch
   integer(c_int64_t),intent(out)::digest,ticks
   integer(c_int),intent(out)::migrated
  end function
  integer(c_int) function native_cpu(ticket,action,sum,ticks) bind(c,name='void_cpu_feedback')
   import c_int,c_int64_t
   integer(c_int64_t),value::ticket
   integer(c_int),value::action
   integer(c_int64_t),intent(out)::sum,ticks
  end function
 end interface
contains
 subroutine require(ok,msg)
  logical,intent(in)::ok
  character(*),intent(in)::msg
  if(.not.ok)then
   write(error_unit,'(a)')'VOID_FORTRAN_FAIL: '//msg
   error stop 3
  end if
 end subroutine
 function upper(s) result(y)
  character(*),intent(in)::s
  character(len(s))::y
  integer::i,k
  y=s
  do i=1,len(s)
   k=iachar(s(i:i));if(k>=97.and.k<=122)y(i:i)=achar(k-32)
  end do
 end function
 function spice_value(s) result(v)
  character(*),intent(in)::s
  character(:),allocatable::t,suffix
  real(dp)::v,mult
  integer::i,ios
  t=trim(upper(adjustl(s)))
  i=1
  do while(i<=len(t))
   if(index('0123456789.+-Ee',t(i:i))==0)exit
   i=i+1
  end do
  call require(i>1,'empty component value')
  read(t(:i-1),*,iostat=ios)v
  call require(ios==0,'bad spice scalar: '//t)
  suffix=t(i:);mult=1.0_dp
  select case(suffix)
  case('');case('T');mult=1e12_dp
  case('G');mult=1e9_dp
  case('MEG');mult=1e6_dp
  case('K');mult=1e3_dp
  case('M');mult=1e-3_dp
  case('U');mult=1e-6_dp
  case('N');mult=1e-9_dp
  case('P');mult=1e-12_dp
  case('F');mult=1e-15_dp
  case default;call require(.false.,'unrecognized SPICE scale: '//suffix)
  end select
  v=v*mult
  call require(ieee_is_finite(v).and.v>0,'nonpositive/nonfinite passive component: '//t)
 end function
 subroutine from_file(path,requested)
  character(*),intent(in)::path
  character(56),intent(in)::requested(:)
  character(2048)::line
  character(56)::label,a,b,value
  logical::found(size(requested))
  integer::j,ios,u,p
  found=.false.
  open(newunit=u,file=path,status='old',action='read',iostat=ios)
  call require(ios==0,'missing circuit source: '//path)
  do
   read(u,'(a)',iostat=ios)line
   if(ios/=0)exit
   if(len_trim(line)==0)cycle
   if(index('*.;',line(1:1))>0)cycle
   p=index(line,' ');if(p==0)cycle
   label=upper(adjustl(line(:p-1)))
   do j=1,size(requested)
    if(label/=requested(j))cycle
    call require(.not.found(j),'duplicate passive label: '//trim(label))
    read(line,*,iostat=ios)label,a,b,value
    call require(ios==0,'invalid passive element: '//trim(line))
    call require(ne<maxelements,'passive elements exceed bound')
    ne=ne+1;elems(ne)%label=trim(label)
    elems(ne)%a=upper(trim(a));elems(ne)%b=upper(trim(b))
    elems(ne)%kind=label(1:1);elems(ne)%value=spice_value(value)
    call require(index('RC',elems(ne)%kind)>0,'unexpected passive kind: '//label)
    found(j)=.true.
   end do
  end do
  close(u)
  call require(all(found),'missing required named component(s) in '//path)
 end subroutine
 integer function nodeindex(label) result(idx)
  character(*),intent(in)::label
  integer::i
  idx=0
  if(label=='0'.or.label=='WRITE_A'.or.label=='WRITE_B')return
  do i=1,nn
   if(nodes(i)==label)then
    idx=i;return
   end if
  end do
  call require(nn<maxnodes,'node bound exceeded')
  nn=nn+1;nodes(nn)=label;idx=nn
 end function
 subroutine read_circuit(root,open_a,open_b)
  character(*),intent(in)::root
  logical,intent(in)::open_a,open_b
  integer::i,ia,ib
  real(dp)::c
  character(:),allocatable::p,q
  p=trim(root)//'/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
  q=trim(root)//'/VOID_K_MESH_V1.lib'
  call require(sha_match(p//c_null_char,k06sha//c_null_char)==1,'K06 sha256 mismatch')
  call require(sha_match(q//c_null_char,meshsha//c_null_char)==1,'mesh sha256 mismatch')
  ne=0;nn=0;conduct=0;capac=0;state=0;nodes=''
  call from_file(p,core)
  call from_file(q,mesh)
  do i=1,ne
   if(open_a.and.elems(i)%label=='C_WRITE_A_COUPLING')cycle
   if(open_b.and.elems(i)%label=='C_WRITE_B_COUPLING')cycle
   ia=nodeindex(elems(i)%a);ib=nodeindex(elems(i)%b)
  end do
  do i=1,ne
   if(open_a.and.elems(i)%label=='C_WRITE_A_COUPLING')cycle
   if(open_b.and.elems(i)%label=='C_WRITE_B_COUPLING')cycle
   ia=nodeindex(elems(i)%a);ib=nodeindex(elems(i)%b)
   if(elems(i)%kind=='R')then
    c=1.0_dp/elems(i)%value
    call stamp(conduct,ia,ib,c)
   else
    c=elems(i)%value
    call stamp(capac,ia,ib,c)
   end if
  end do
  call require(nn>0,'no circuit nodes')
  olda=0;oldb=0;elapsed=0
 end subroutine
 subroutine stamp(m,a,b,k)
  real(dp),intent(inout)::m(:,:)
  integer,intent(in)::a,b
  real(dp),intent(in)::k
  if(a/=0)m(a,a)=m(a,a)+k
  if(b/=0)m(b,b)=m(b,b)+k
  if(a/=0.and.b/=0)then
   m(a,b)=m(a,b)-k;m(b,a)=m(b,a)-k
  end if
 end subroutine
 real(dp) function vfixed(name,a,b)result(v)
  character(*),intent(in)::name
  real(dp),intent(in)::a,b
  v=0
  if(name=='WRITE_A')v=a
  if(name=='WRITE_B')v=b
 end function
 subroutine right_fixed(kind,a,b,rhs)
  character,intent(in)::kind
  real(dp),intent(in)::a,b
  real(dp),intent(out)::rhs(:)
  integer::i,ia,ib
  real(dp)::k
  rhs=0
  do i=1,ne
   if(elems(i)%kind/=kind)cycle
   ! source disconnects are applied by caller via active logical mask
   if(active_skip(i))cycle
   ia=findindex(elems(i)%a);ib=findindex(elems(i)%b)
   if(kind=='R')then
    k=1.0_dp/elems(i)%value
   else
    k=elems(i)%value
   end if
   if(ia/=0.and.ib==0)rhs(ia)=rhs(ia)+k*vfixed(elems(i)%b,a,b)
   if(ib/=0.and.ia==0)rhs(ib)=rhs(ib)+k*vfixed(elems(i)%a,a,b)
  end do
 end subroutine
 logical function active_skip(i)
  integer,intent(in)::i
  active_skip=(skip_a.and.elems(i)%label=='C_WRITE_A_COUPLING').or. &
              (skip_b.and.elems(i)%label=='C_WRITE_B_COUPLING')
 end function
 integer function findindex(s)result(i)
  character(*),intent(in)::s
  integer::j
  i=0
  if(s=='0'.or.s=='WRITE_A'.or.s=='WRITE_B')return
  do j=1,nn
   if(nodes(j)==s)then
    i=j;return
   end if
  end do
  call require(.false.,'unknown source node: '//s)
 end function
 subroutine reset_state(open_a,open_b)
  logical,intent(in)::open_a,open_b
  skip_a=open_a;skip_b=open_b
  state=0;olda=0;oldb=0;elapsed=0
 end subroutine
 subroutine solve_step(dt,a,b)
  real(dp),intent(in)::dt,a,b
  real(dp)::lhs(maxnodes,maxnodes),rhs(maxnodes),oldc(maxnodes),newc(maxnodes),gr(maxnodes)
  integer::piv(maxnodes),info
  call require(ieee_is_finite(dt).and.dt>0,'bad dt')
  call require(ieee_is_finite(a).and.ieee_is_finite(b).and.a>=0.and.a<=1.3_dp.and. &
       b>=0.and.b<=1.3_dp,'drive out of range')
  call right_fixed('C',olda,oldb,oldc);call right_fixed('C',a,b,newc)
  call right_fixed('R',a,b,gr)
  lhs=conduct+capac/dt
  rhs=matmul(capac,state)/dt+(newc-oldc)/dt+gr
  call dgesv(nn,1,lhs,maxnodes,piv,rhs,maxnodes,info)
  call require(info==0,'LAPACK DGESV singular/error')
  call require(all(ieee_is_finite(rhs(:nn))),'nonfinite solve output')
  state(:nn)=rhs(:nn);olda=a;oldb=b;elapsed=elapsed+dt
 end subroutine
 real(dp) function get_voltage(label)result(v)
  character(*),intent(in)::label
  integer::i
  i=findindex(label)
  call require(i/=0,'missing requested node: '//label)
  v=state(i)
 end function
 real(dp) function capacitor_energy()result(e)
  integer::i
  real(dp)::a,b
  e=0
  do i=1,ne
   if(elems(i)%kind/='C'.or.active_skip(i))cycle
   a=value_at(elems(i)%a);b=value_at(elems(i)%b)
   e=e+0.5_dp*elems(i)%value*(a-b)**2
  end do
 end function
 real(dp) function value_at(s)result(v)
  character(*),intent(in)::s
  integer::i
  i=findindex(s)
  if(i==0)then
   v=vfixed(s,olda,oldb)
  else
   v=state(i)
  end if
 end function
 subroutine cpu_feedback(ticket,action,checksum,cycles)
  integer(c_int64_t),intent(in)::ticket
  integer,intent(in)::action
  integer(c_int64_t),intent(out)::checksum,cycles
  integer(c_int)::status
  status=native_cpu(ticket,int(action,c_int),checksum,cycles)
  call require(status==0,'native AVX2 feedback failed; status '//itoa(status))
 end subroutine
 subroutine cpu_init()
  integer(c_int)::status
  status=native_cpu_init()
  call require(status==0,'native CPU feature gate failure: '//itoa(status))
 end subroutine
 subroutine cpu_execute(sel,epoch,digest,ticks,migrated)
  integer,intent(in)::sel,epoch
  integer(c_int64_t),intent(out)::digest,ticks
  integer(c_int),intent(out)::migrated
  integer(c_int)::status
  status=native_cpu_work(int(sel,c_int),int(epoch,c_int),digest,ticks,migrated)
  call require(status==0.and.ticks>0,'CPU-native feedback cycle failed: '//itoa(status))
 end subroutine
 subroutine native_decision(exe,a,b,s,bit)
  character(*),intent(in)::exe
  integer,intent(in)::a,b
  integer,intent(out)::s,bit
  integer(c_int)::cs,cb,status
  status=native_eval(trim(exe)//c_null_char,int(a,c_int),int(b,c_int),cs,cb)
  call require(status==0,'native HX89 execution failed; code '//itoa(status))
  s=int(cs);bit=int(cb)
 end subroutine
 function itoa(i)result(s)
  integer,intent(in)::i
  character(20)::s
  write(s,'(i0)')i
 end function
end module

program void_loop
 use, intrinsic :: iso_fortran_env, only:real64,error_unit
 use, intrinsic :: iso_c_binding, only:c_int,c_int64_t
 use void_rc
 implicit none
 integer,parameter::dp=real64, steps=96, substeps=12
 character(1024)::source,exe,dest,scenario,file1,file2
 character(24),parameter::scenarios(7)=[character(24)::'closed_loop','closed_loop_repeat', &
  'open_write_a','no_excitation','forced_a','inverted_action','open_write_b']
 integer::i,j,k,bit_a,bit_b,s,bit,selected,u,v,ones,ios,overall
 integer(c_int64_t)::cpu_digest,cpu_ticks
 integer(c_int)::cpu_migrated
 integer(c_int64_t)::checksum,cycles
 real(dp)::va,vb,a,b,max_a,max_b,max_c,end_a,end_b,end_c
 if(command_argument_count()/=3)then
  write(error_unit,'(a)')'usage: void_loop SOURCE_DIR HX89_BINARY OUTPUT_DIR'
  stop 2
 end if
 call get_command_argument(1,source);call get_command_argument(2,exe);call get_command_argument(3,dest)
 open(newunit=overall,file=trim(dest)//'/native_summary.csv',status='replace',action='write',iostat=ios)
 if(ios/=0)error stop 'output directory missing'
 write(overall,'(a)')'scenario,steps,native_ones,max_charge_a,max_charge_b,max_charge_c,end_charge_a,end_charge_b,end_charge_c'
 do k=1,size(scenarios)
  scenario=trim(scenarios(k));file1=trim(dest)//'/'//trim(scenario)//'_native.csv'
  file2=trim(dest)//'/'//trim(scenario)//'_trajectory.csv'
  call read_circuit(trim(source),k==3,k==7)
  call reset_state(k==3,k==7)
  call cpu_init()
  open(newunit=u,file=trim(file1),status='replace',action='write',iostat=ios)
  if(ios/=0)error stop 'native trace create failed'
  open(newunit=v,file=trim(file2),status='replace',action='write',iostat=ios)
  if(ios/=0)error stop 'trajectory create failed'
  write(u,'(a)')'step,observed_charge_a_v,observed_charge_b_v,adc_a,adc_b,native_sum,native_bit,selected,drive_a_v,drive_b_v,cpu_cycle_digest,cpu_cycle_tsc_ticks,cpu_migrated,cpu_feedback_checksum,cpu_feedback_tsc_ticks'
  write(v,'(a)')'step,substep,time_s,drive_a_v,drive_b_v,charge_a_v,charge_b_v,charge_c_v,probe_a_v,probe_b_v,energy_j'
  max_a=0;max_b=0;max_c=0;ones=0
  do i=0,steps-1
   va=get_voltage('CHARGE_A');vb=get_voltage('CHARGE_B')
   bit_a=0;bit_b=0
   if(va>=0.006_dp)bit_a=1
   if(vb>=0.006_dp)bit_b=1
   call native_decision(trim(exe),bit_a,bit_b,s,bit)
   if(s/=bit_a+bit_b.or.bit/=max(bit_a,bit_b))error stop 'native oracle conflict'
   ones=ones+bit;selected=bit
   if(k==5)selected=0
   if(k==6)selected=1-selected
   call cpu_execute(selected,i,cpu_digest,cpu_ticks,cpu_migrated)
   a=0;b=0
   if(k/=4)then
    if(selected==0)a=1.2_dp
    if(selected==1)b=1.2_dp
   end if
   call cpu_feedback(int(k*1000+i,c_int64_t),selected,checksum,cycles)
   write(u,'(*(g0,:,","))')i,va,vb,bit_a,bit_b,s,bit,selected,a,b,cpu_digest,cpu_ticks,cpu_migrated,checksum,cycles
   do j=0,substeps-1
     if(j<9)then
     call solve_step(0.004_dp/substeps,a,b)
    else
     call solve_step(0.004_dp/substeps,0.0_dp,0.0_dp)
    end if
    end_a=get_voltage('CHARGE_A');end_b=get_voltage('CHARGE_B');end_c=get_voltage('CHARGE_C')
    max_a=max(max_a,abs(end_a));max_b=max(max_b,abs(end_b));max_c=max(max_c,abs(end_c))
    if(j<9)then
     write(v,'(*(g0,:,","))')i,j, (i*substeps+j+1)*(0.004_dp/substeps),a,b, &
      end_a,end_b,end_c,get_voltage('PROBE_A'),get_voltage('PROBE_B'),capacitor_energy()
    else
     write(v,'(*(g0,:,","))')i,j, (i*substeps+j+1)*(0.004_dp/substeps),0.0_dp,0.0_dp, &
      end_a,end_b,end_c,get_voltage('PROBE_A'),get_voltage('PROBE_B'),capacitor_energy()
    end if
   end do
  end do
  write(overall,'(*(g0,:,","))')trim(scenario),steps,ones,max_a,max_b,max_c,end_a,end_b,end_c
  write(*,'(a,1x,a,1x,i0,1x,3(es14.6,1x))')'NATIVE_PASS',trim(scenario),ones,end_a,end_b,end_c
  close(u);close(v)
 end do
 close(overall)
end program
