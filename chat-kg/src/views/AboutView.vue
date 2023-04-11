<template>
  <div class="about">
    <img class="logo" src="/logo_jnu.svg" alt="">
    <h2>江南大学先进技术研究院介绍</h2>
    <p>先进技术研究院是江南大学直属科研单位，通过人才引培、科研创新、成果转化，开展基础理论与实际应用相结合的产学研合作，着重围绕共性核心关键技术，聚焦工业软件、高端装备硬件和新型材料器件等重点领域，开展“软件+硬件+器件”三位一体的科学技术研究和科技成果转化。目前有半导体传感器件与集成电路、新型集成电路和射频电路、光电集成与传感检测、宽禁带/超宽禁带半导体材料与器件、机械结构强度与多尺度力学、精密智能系统工程、增材制造材料与工艺、微纳制造柔性电子、模式识别与计算智能、耐极端环境复合材料与结构等10个团队。现有教师（含博士后）61名、研究生362名，开展基础理论与实际应用相结合的产学研合作。


    </p>
    <h2>研究院的背景与目标</h2>
    <p>江南大学先进技术研究院是江南大学的重要研究机构之一，其成立旨在引领国内先进技术的研究和应用，推动技术创新和产业转型升级。研究院的目标是培养高水平的科技创新人才，为国家和地方的经济发展做出积极的贡献</p>
    <h2>人工智能与自然语言处理</h2>
    <p>作为江南大学先进技术研究院的重点研究方向之一，人工智能和自然语言处理的研究内容涉及到语言模型、机器翻译、信息抽取、文本分类等方面。研究院的科学家们不断探索和创新，力争取得在该领域的突破性进展。</p>
    <h2>计算机视觉</h2>
    <p>计算机视觉是江南大学先进技术研究院的另一个重点研究方向。其研究内容包括图像识别、目标检测、图像分割、三维重建等方面。通过对计算机视觉技术的研究和创新，研究院的科学家们旨在实现更加智能化和精准化的图像处理和分析。</p>
    <h2>学科建设和人才培养</h2>
    <p>江南大学先进技术研究院在人才培养方面也下了很大的功夫。研究院设有博士后研究流动站，与众多国内外知名高校和研究机构合作开展合作交流，积极培养具有国际视野和创新精神的科研人才。同时，研究院也不断加强学科建设，吸引更多优秀的学生和研究人员加入到该领域的研究中来。</p>

    <footer>
      <p>© 2023 <a href="http://iat.jiangnan.edu.cn/" target="_blank">江南大学先进技术研究院</a></p>
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
