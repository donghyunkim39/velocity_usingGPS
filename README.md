# velocity_usingGPS

> For user who: GPS 위도(latitude), 경도(longitude)와 GPS topic이 publish되는 시간으로 속력을 구하고싶은 user, 자율주행자동차를 구현하기 위해 현재속도를 구해야하는데 현재속도를 하나의 topic으로 publish되길 원하는 user

>원리: haversine라이브러리를 이용해 두지점을 이동한 거리를 구하고, 두지점을 지나는데 걸리는 시간을 구하여 속력 = 변위(거리) / 시간 을 통해 속력을 구한다.

>준비물: 

1) 위도, 경도를 실시간으로 출력해주는 topic (필자의 경우 /gps/fix 토픽임)
![Screenshot from 2024-04-28 04-20-26](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/5aed531d-fdfc-479f-bd85-0473e8756716)

![Screenshot from 2024-04-28 04-20-54](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/b20ad6a9-6949-4708-ba34-729eb8e0f100)

ubuntu 명령창에 아래코드를 입력하면 위 사진과 같은 topic들을 볼수있다.
```bash
rostopic list
```

>우리가 사용할 정보는 topic 정보중에 시간(secs, nsecs), 위도(latitude), 경도(longitude) 이다.
> ex) 첫지점의 (위도,경도,시간)이 Location1(35.240451156243284, 126,8411777433688, 1713758627.594646408초)
>     이동한 지점이 Location2(35.230451156243284, 126.8411777433688, 1713758627.617737960초) 라면

>haversine라이브러리를 활용해 위도,경도 정보로 거리를 구하고, Location1에서 Location2까지 이동하는데 걸린 시간차(1713758627.617737960초- 1713758627.594646408초) 를 구하여
>속력 = 거리/시간 으로 구한다.

## Code

![스크린샷 2024-04-28 043045](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/8a291a04-8a2b-4c6c-a7fc-41e317b27e12)

## Code 분석

![스크린샷 2024-04-28 043045](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/6ea18c6c-e909-419f-813b-a99623c799b5)
> 1) rospy.Subscriber에서 받아올 topic이름은 필자의 경우 /gps/fix이며, 이때 토픽의 메시지 유형은 NavSatFix 이다.
> 토픽 이름과 그토픽의 유형은 rostopic list 와 rostopic info '토픽이름' 명령어를 통해 수정하는 사람에 맞게 변경한다.


![스크린샷 2024-04-28 045404](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/ec490360-0cb5-435a-832b-cf981a16c5be)
> 2) publish되는 주기를 설정한다. 주기를 설정하지 않으면 /gps/fix 토픽을 너무 자주 subscribe하게 되므로 추후 pid제어시 너무 빈번한 종방향제어를 하게된다.
> ex) 5초마다 subscribe하고 싶으면 1/5 =0.2, 4초마다 subscribe하고 싶으면 1/4 = 0.25를 적어준다.


![스크린샷 2024-04-28 045504](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/cb179697-9911-4b87-9ba8-8ae4e4e91aa1)
> 3) fix_callback 메소드이다. /gps/fix 토픽에는 위도,경도,시간말고도 더많은 정보를 담고있는데 이중에서 어떤 데이터를 받아올건지 설정하는 부분이다.
> self.second = self.secs + self.nsecs * 10^-9 를 한이유는 코드 그대로 self.secs가 자연수 단위초를 self.nsecs가 나노(10^-9)단위 초를 담고있기때문이다.


![스크린샷 2024-04-28 045832](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/08a626be-c910-4b06-9f46-6d4a1c73113b)
> 4) velocity 메소드이다. 두지점을 이동하는데 걸리는 시간을 self.time_diff 변수에 담고있다.



![스크린샷 2024-04-28 050055](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/08b96f05-a566-440c-bbb7-0f58e4e08d18)
> 5) distance 메소드이다. 두지점을 사이의 거리를 haversine라이브러리를 통해 구한다. 곱하기1000을 한이유는 haversine을 통해 구한 거리가 km이므로 m로 변환한것이다.


![스크린샷 2024-04-28 050200](https://github.com/donghyunkim39/velocity_usingGPS/assets/163104650/1ed1d25e-4df1-4bc9-9ed2-0360803225b1)
> 6) calculate 메소드이다. 위에서 구한 시간과 거리값을 이용해 속력 = 거리/시간을 실질적으로 계산하는 메소드이다.
>    
> 계산한 m/s 단위의 속력을 /now_velocity라는 topic으로 출력한다. 이때 메시지 유형은 Float64 이다.


