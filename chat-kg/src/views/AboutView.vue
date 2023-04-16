<template>
  <div class="about">
    <img class="logo" src="/logo_jnu.svg" alt="">
    <h2>江南大学先进技术研究院介绍</h2>
    <p>
      先进技术研究院是江南大学直属科研单位，通过人才引培、科研创新、成果转化，开展基础理论
      与实际应用相结合的产学研合作，着重围绕共性核心关键技术，聚焦工业软件、高端装备硬件和新
      型材料器件等重点领域，开展“软件+硬件+器件”三位一体的科学技术研究和科技成果转化。目前有
      半导体传感器件与集成电路、新型集成电路和射频电路、光电集成与传感检测、宽禁带/超宽禁带
      半导体材料与器件、机械结构强度与多尺度力学、精密智能系统工程、增材制造材料与工艺、微纳
      制造柔性电子、模式识别与计算智能、耐极端环境复合材料与结构等10个团队。现有教师（含博士
      后）61名、研究生362名，开展基础理论与实际应用相结合的产学研合作。
    </p>
    <img src="/230412005841.png" alt="">
    <h2>研究院的背景与目标</h2>
    <p>
      研究院目前拥有省工程实验室，江苏省模式识别与计算智能工程实验室由江苏省发展与改革委员会
      批准建设，实验室主任为吴小俊教授。目前实验室拥有一支梯队结构合理、以中青年教师为主的高
      水平师资队伍。实验室研究方向为模式识别理论与技术、计算智能理论与技术、智慧城市与物联网
      应用。在国内外学术期刊和会议上共发表高水平学术论文400余篇，取得了一批国内领先、有广泛
      推广应用价值的成果，部分成果达到国际先进水平。
    </p>
    <h2>学科建设和人才培养</h2>
    <p>
      学院建立了完善的人才培养机制，培养成效显著。计算机科学与技术专业、数字媒体技术专业在课
      程教学和人才培养模式创新方面分别获得江苏省教学成果二等奖；本科生多次在国内外竞赛中获得
      佳绩，如获得美国数学建模大赛一等奖、国际视觉目标跟踪大赛（VOT2020）冠军、ICCV2021国
      际竞赛冠军、ACM国际大学生程序设计竞赛银奖、中国“互联网+”大学生创新创业大赛金奖、全国
      大学生网络安全精英赛金奖、中国大学生服务外包创新创业大赛一等奖、中国大学生计算机设计大
      赛一等奖、全国大学生数字媒体科技作品及创意竞赛一等奖等。毕业生广泛就业于微软公司、网易
      公司、中国移动公司、百度、阿里、腾讯、中国船舶重工集团公司第七二三研究所等各大知名企业
      及相关院校和科研单位。
    </p>
    <footer>
      <p>© 2023 <a href="http://iat.jiangnan.edu.cn/" target="_blank">A27</a></p>
    </footer>
  </div>
</template>

<style lang="less" scoped>
.about {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #333;
  width: 80%;
  max-width: 800px;
  min-height: calc(100vh - 200px);
  margin: 0 auto;
  margin-top: 40px;
  // text-align: center;
  font-family: 'HarmonyOS Sans SC', 'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'ST Heiti', 'SimHei', 'WenQuanYi Zen Hei Sharp', 'Droid Sans Fallback', 'Droi';
}

img.logo {
  width: 300px;
  // height: 100px;
  margin: 2rem auto;
}

img {
  max-width: 100%;
  margin: 1rem auto;
  object-fit: contain;
  border-radius: 8px;
}

h2 {
  width: 100%;
  font-size: 1.2rem;
  line-height: 1.2rem;
  margin: 1em 0;
  border-left: 5px solid #005f77;
  padding-left: 0.8em;
}

p {
  font-size: 1rem;
  line-height: 1.8em;
  margin: 0.5em 0;
}


footer {
  margin-top: auto;
  text-align: center;
  font-size: 0.8em;
  color: #999;

  a {
    color: #999;
  }
}

</style>
