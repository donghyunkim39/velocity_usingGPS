# velocity_usingGPS

> For user who: GPS 위도(latitude), 경도(longitude)와 GPS topic이 publish되는 시간으로 속력을 구하고싶은 user, 자율주행자동차를 구하기 위해 현재속도를 구해야하는데 현재속도를 하나의 topic으로 publish되길 원하는 user

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


