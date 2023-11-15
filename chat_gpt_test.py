from openai import OpenAI

if __name__ == '__main__':
    concert_content = '\n<p><span style=><span style="font-family: , sans-serif;">聲色犬王 is back！<br></span><span style="font-family: , sans-serif;">睽違10年，MC HotDog熱狗「髒藝術家」再臨小巨蛋。<br></span><span style="font-family: , sans-serif;"><br>「其實我們每一個人都是藝術家，因為活著本身他媽的就是一門藝術啊！」<br></span><span style="font-family: , sans-serif;"><br></span><span style="font-family: , sans-serif;">風風雨雨、是是非非，keep real的饒舌歌手就算銅鑄鐵打，也躲不過奴儒道德的天羅地網。你看看每個人都站在道德制高點對他掏槍，但MC HotDog熱狗態度依舊坦蕩，因為他就是最屌的髒藝術家，是牛屎上最香的一束花！<br><br></span><span style="font-family: , sans-serif;">看到這，別擔心，演唱會不會出現牛屎，但保證讓你嗨到流目屎。本色出品，看過的都有信心！最好玩的演唱會，就在本色音樂！<br><br></span><span style="font-family: , sans-serif;">MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會，12/23-24 邀你一起來派對！<br><br></span><span style="font-family: , sans-serif;">【<strong>MC HotDog</strong><strong>熱狗「髒藝術家」</strong><strong>2023</strong><strong>台北小巨蛋演唱會</strong>】<br></span><span style="font-family: , sans-serif;"><strong>演出時間：</strong>2023/12/23 (六) 19:00開演（18:00入場，預定21:30結束）</span></span><br><span style=><span style="font-family: , sans-serif;">　　　　　2023/12/24 (日) 16:30開演（15:30入場，預定19:00結束）<br></span><span style="font-family: , sans-serif;"><strong>演出地點：</strong>台北小巨蛋<br><br></span><span style="font-family: , sans-serif;"><strong>售票時間：<br></strong></span><span style="font-family: , sans-serif;"><strong>2023/11/04&nbsp;(</strong><strong>六</strong><strong>)11:00</strong><strong>～</strong><strong>2023/11/10&nbsp;(</strong><strong>五</strong><strong>)18:00<br></strong></span><span style="font-family: , sans-serif;">11:00 ➤本色會員優先購票</span></span><br><span style="font-family: , sans-serif; font-size: 15px;"> 13:00 ➤本色會員一般購票<br><span style="color: #0000ff;"><strong>（僅限本色會員購票）</strong></span><br></span></p><p><span style=><span style="color: #0000ff; font-family: , sans-serif;"><strong>本色售票網：<a href="https://truecolormusic.tixcraft.com/activity" target="_blank" style="color: #0000ff;">https://truecolormusic.tixcraft.com/activity</a></strong></span><span style="font-family: , sans-serif;"><strong><br><br>會員早鳥票：<br></strong></span><span style="font-family: , sans-serif;">藝術特區、中二特區、差不多特區、貧民百萬特區、廢物特區3880<br></span><span style="font-family: , sans-serif;">座位區3880/3580/2980/2300/2000/1800/1500/800<br></span><span style="font-family: , sans-serif;"><strong>身障及陪同票</strong> 400<br><br></span><span style="font-family: , sans-serif;"><strong>售票時間：<br></strong></span><span style="font-family: , sans-serif;"><strong>2023/11/11&nbsp;(六)&nbsp;<br> </strong>11:00 ➤拓元售票系統會員購票<br></span><span style="font-family: , sans-serif;"><strong>全票：<br></strong></span><span style="font-family: , sans-serif;">藝術特區、中二特區、差不多特區、貧民百萬特區、廢物特區<span>4380</span><br></span><span style="font-family: , sans-serif;">座位區4380/4080/3480/2800/2400/2200/1800/800<br></span><span style="font-family: , sans-serif;"><strong>身障及陪同票</strong> 400<br><br></span><span style="font-family: , sans-serif;">主辦單位：本色音樂/滾石唱片</span></span><br><span style="font-family: , sans-serif; font-size: 15px;"> 協辦單位：台灣滾石音樂經紀股份有限公司/兄弟本社</span></p>                    \x3C!-- start: 節目圖檔 -->\n                    <div class="thumbnail">\n                        <h5 class="text-primary">\n                            示意圖僅供參考示意                        </h5>\n<p><img src="https://static.tixcraft.com/images/activity/field/23_mchotdog_10666ebcbf84c575e447f013baf5ce38.jpg" width="400" alt="示意圖僅供參考示意1" title="點圖放大" style="cursor: pointer;"></p>                    </div>\n                    \x3C!-- end: 節目圖檔 -->\n  '

    client = OpenAI(
        api_key="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",
    )
    # openai.api_key = os.getenv('OPEN_AI_KEY')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You will be provided with unstructured chinese html text, and your task is to parse it into json format like this {'concert_title': string, 'concert_time': list of YYYY-MM-E hh:mm, 'sell_ticket_time': list of  YYYY-MM-EE hh:mm, concert_singer: string ,concert_location:string}."},
            {"role": "user", "content": concert_content}
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=500
    )

    response = completion.choices[0].message
    data = getattr(response, 'content')
    print(data)
    print(type(data))