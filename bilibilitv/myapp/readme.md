get_video_url:

http://host/myapp/video/?page=1&url=http://www.bilibili.tv/video/av409923/

params: 
    page: the video part number if there are many piece of this video
    url:  the origin video url in bilibili

return value:
   
    json format data of video url which has converted to mp4 for mobile 

    {
    "url":"http://bilibili-tv.oss.aliyuncs.com:80/video/2013-11-15/smosh%E6%99%BA%E7%88%B7%E6%95%99%E4%BD%A0%E5%96%9D%E5%B0%BF%E6%B1%82%E7%94%9F.mp4"
    } 

    error or 404 response when error occured

get_video_subtitle:

http://host/myapp/comment/?page=1&url=http://www.bilibili.tv/video/av409923/

params 
    page: like up
    url: like up

return value:

    json format data about the video information and the subtitle information

    about comment_source:

        p:
            the suttitle params:
            
                like:

                    {
                    "p":"120.13200378418,1,25,16777215,1348297863,0,1e593f97,131382166",

                    "text":"贝爷明显残念"
                    },
                    1.the time about second
                    2.the subtitle type:
                        1.scroll subtitle (right ~ left)
                        2....
                        3....
                        4.bottom subtitle
                        5.top subtitle
                        6.revese subtitle
                        7.locate subtitle
                        8.advance subtitle
                    3.font size:
                        12
                        16
                        18
                        25
                        36
                        45
                        64
                    4.subtitle html color
                    5.comment time ,base time is 1970-1-1 08:00:00
                    6.subtitle pool:
                        0:normal
                        1.subtitle pool
                    7.user id,can filter to block
                    8.history subtitle function
