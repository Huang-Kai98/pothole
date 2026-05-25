# 道路坑洞检测 / 视觉大模型辅助避障数据集中文报告

本文档面向“道路坑洞检测 / 视觉大模型辅助避障”项目，按数据集说明其来源、主要作用、适用范围、注意事项和推荐引用。  
建议将本文档作为数据选型和实验设计入口，不建议直接把所有数据集混合训练；应先完成原始数据归档、格式检查、统一 manifest、统计报告和许可证确认。

## 总体选型建议

| 数据集 | 主要价值 | 推荐用途 |
|---|---|---|
| HRP4K | 高分辨率、真实道路透视视角、含负样本 | 主力坑洞检测基准、小目标检测、误检分析 |
| UDTIRI | 检测、语义分割、实例分割均可支持 | 视觉大模型基准、实例分割、多任务评估 |
| RDD2022 / RDD2020 | 多国家道路损伤检测，含 D40 坑洞 | D40 坑洞抽取、域泛化、裂缝 hard negative |
| NPD | 夜间/低照度坑洞 | 夜间避障、低照度鲁棒性测试 |
| Water-Filled and Dry Potholes | 干坑/积水坑 | 雨后、湿路面、水坑误检控制 |
| Pothole Mix | 坑洞/裂缝语义分割，含 RGB-D 视频 | 分割、数据增强、RGB-D 辅助避障 |
| Pothole-600 / Rui Fan Stereo | 双目、视差、像素级标签、3D 线索 | 深度辅助避障、几何验证、3D 感知 |
| Cracks and Potholes in Road Images | road/crack/pothole 三类 mask | 道路区域约束、联合分割 |
| MWPD | 多天气、多光照 | 雨天、黄昏、夜间鲁棒性 |
| UAV RoadAnomaly-YOLO | UAV + 地面视角，道路异常多类 | 无人机巡检、跨视角迁移 |
| RoadDamageVision | 道路损伤多类，含 D40 | 类别不均衡、域适应 |
| Roboflow/Kaggle Pothole | 小型检测数据 | 快速 demo、脚本冒烟测试 |
| Road Damage: Potholes, Cracks and Manholes | 坑洞/裂缝/井盖 | 井盖 hard negative，降低井盖误检 |

## 1. HRP4K

- 来源：Zenodo / 论文数据页；论文为 *A high-resolution perspective-view road image dataset for pothole detection*。
- 作用：提供高分辨率 4K 透视道路图像，专门用于坑洞目标检测。
- 适用范围：小目标坑洞检测、远距离检测、复杂背景误检分析、真实车载视角评测。
- 标注与类别：YOLO 和 COCO bbox；类别为 pothole；含正样本和负样本。
- 规模信息：论文摘要说明包含 6,003 张图像、4,003 张正样本、2,000 张负样本、7,217 个坑洞实例。
- 项目建议：可作为主检测基准之一；负样本适合控制阴影、污渍、井盖等误检。
- 限制：需确认下载页许可证和再分发限制；高分辨率训练时显存压力较大。
- 推荐引用：*A high-resolution perspective-view road image dataset for pothole detection*, Scientific Data, 2026。  
  链接：https://www.nature.com/articles/s41597-026-07317-w

## 2. UDTIRI

- 来源：Kaggle `jiahangli617/udtiri`；论文为 *UDTIRI: An Online Open-Source Intelligent Road Inspection Benchmark Suite*。
- 作用：面向智能道路巡检的开放基准，首个任务聚焦道路坑洞检测。
- 适用范围：目标检测、语义分割、实例分割、视觉大模型识别/定位基准。
- 标注与类别：COCO JSON、像素/实例级标注；类别以 pothole 为主。
- 规模信息：论文摘要说明包含 1,000 张 RGB 图像及像素/实例级真值标注。
- 项目建议：优先用于 segmentation/VLM benchmark；也可从 COCO bbox 转 YOLO detect。
- 限制：需遵守 Kaggle 条款；转换前应检查 COCO 类别名和 mask 编码方式。
- 推荐引用：*UDTIRI: An Online Open-Source Intelligent Road Inspection Benchmark Suite*, arXiv:2304.08842。  
  链接：https://arxiv.org/abs/2304.08842

## 3. RDD2022

- 来源：Kaggle `aliabdelmenam/rdd-2022`；原始数据来自 CRDDC 2022 / RDD2022。
- 作用：多国家道路损伤检测数据集，适合评估模型跨地区泛化。
- 适用范围：D40 坑洞抽取、道路损伤多类检测、裂缝作为 hard negative、多国家域适应。
- 标注与类别：Pascal VOC XML；D00 纵向裂缝、D10 横向裂缝、D20 龟裂、D40 坑洞。
- 规模信息：论文说明含 47,420 张道路图像、超过 55,000 个道路损伤实例，覆盖日本、印度、捷克、挪威、美国、中国。
- 项目建议：默认用 `convert_rdd_d40_to_yolo.py --mode pothole_only` 将 D40 统一为 pothole；多类实验可保留 D00/D10/D20/D40。
- 限制：D40 相对裂缝类别更少，类别不均衡明显；不同国家图像域差异较大。
- 推荐引用：*RDD2022: A multi-national image dataset for automatic Road Damage Detection*, arXiv:2209.08538。  
  链接：https://arxiv.org/abs/2209.08538

## 4. RDD2020

- 来源：Mendeley Data DOI `10.17632/5ty2wb6gvg.1`；论文为 *RDD2020: An annotated image dataset for automatic road damage detection using deep learning*。
- 作用：RDD 系列早期版本，多地区道路损伤检测。
- 适用范围：D40 坑洞抽取、与 RDD2022 做时间/版本对比、道路损伤多类检测。
- 标注与类别：Pascal VOC XML；D00、D10、D20、D40。
- 规模信息：论文页面说明含 26,336 张道路图像，超过 31,000 个道路损伤实例，覆盖印度、日本和捷克。
- 项目建议：与 RDD2022 分开统计，不要直接混合；D40 映射为 pothole。
- 限制：需手动下载并确认 Mendeley 使用条款；类别和目录结构可能与 RDD2022 不完全一致。
- 推荐引用：*RDD2020: An annotated image dataset for automatic road damage detection using deep learning*, Data in Brief, 2021。  
  链接：https://pmc.ncbi.nlm.nih.gov/articles/PMC8166755/

## 5. NPD Nighttime Pothole Dataset

- 来源：GitHub `https://github.com/hhaozhang/NPD`；Google Drive file id `1F7IBMEwf25ZVgJC2RrqbCbiuZM-wc1f0`。
- 作用：夜间坑洞检测基准，弥补白天数据偏置。
- 适用范围：低照度、夜间、车灯照明、暗背景误检分析、夜间避障模型评估。
- 标注与类别：以 pothole detection 为主；下载后需检查具体标注格式。
- 规模信息：论文摘要说明 NPD 包含 3,831 张夜间场景图像。
- 项目建议：不要与白天数据简单混合；建议单独保留夜间测试集或夜间 domain split。
- 限制：仓库说明包含非商业研究用途限制，使用前需确认。
- 推荐引用：*Nighttime Pothole Detection: A Benchmark*, Electronics, 2024。  
  链接：https://www.mdpi.com/2079-9292/13/19/3790  
  数据链接：https://github.com/hhaozhang/NPD

## 6. Annotated Water-Filled and Dry Potholes

- 来源：Mendeley Data DOI `10.17632/tp95cdvgm8.1`。
- 作用：覆盖积水坑和干坑，补充湿路面场景。
- 适用范围：雨后道路、积水坑、反光区域、湿路面鲁棒性评估。
- 标注与类别：Pascal VOC XML 和 YOLO TXT；类别以 pothole 为主。
- 项目建议：优先检查 VOC 与 YOLO 标注是否一致；可将积水坑作为子域单独统计。
- 限制：需手动下载并确认许可证；积水区域容易与坑洞边界混淆，适合作为误差分析集。
- 推荐引用：Mendeley Data DOI `10.17632/tp95cdvgm8.1`。  
  链接：https://data.mendeley.com/datasets/tp95cdvgm8/1

## 7. Pothole Mix

- 来源：Mendeley Data DOI `10.17632/kfth5g2xk3.2`。
- 作用：坑洞和裂缝语义分割数据集，并提供 RGB-D 视频资源。
- 适用范围：YOLO segment、Mask R-CNN、语义分割、RGB-D 辅助标注、合成增强。
- 标注与类别：image-mask pairs；pothole + crack；附 RGB-D 视频。
- 规模信息：Mendeley 页面说明主数据集为 4,340 对 image/mask，训练/验证/测试约为 3340/496/504；另含 797 个 RGB-D clips 和对应 disparity clips。
- 项目建议：适合训练分割模型；mask 转 YOLO segmentation 前必须检查像素编码。
- 限制：版本 2 许可证为 Attribution-NonCommercial 3.0 Unported，商业使用需谨慎。
- 推荐引用：Pothole Mix, Mendeley Data, V2, DOI `10.17632/kfth5g2xk3.2`。  
  链接：https://data.mendeley.com/datasets/kfth5g2xk3/2

## 8. Pothole-600

- 来源：数据页 `https://sites.google.com/view/pothole-600/dataset`。
- 作用：双目/RGB-D 坑洞语义分割数据集。
- 适用范围：深度辅助避障、语义分割、视差图融合、坑洞深度几何分析。
- 标注与类别：RGB、disparity / transformed disparity、pixel-level pothole label。
- 规模信息：综述与相关论文常引用其 600 张图像、ZED stereo camera、400 x 400、像素级 pothole 标注。
- 项目建议：不要只转成 2D bbox；应保留 RGB 与视差对应关系，用于避障实验。
- 限制：下载和使用需遵守数据页说明；深度/视差预处理链路需要记录。
- 推荐引用：Pothole-600 dataset page；相关方法论文 *Multi-Scale Feature Fusion: Learning Better Semantic Segmentation for Road Pothole Detection*。  
  数据链接：https://sites.google.com/view/pothole-600/dataset  
  论文链接：https://arxiv.org/abs/2112.13082

## 9. Rui Fan Stereo Pothole Datasets

- 来源：GitHub `https://github.com/ruirangerfan/stereo_pothole_datasets`。
- 作用：早期公开的多模态道路坑洞数据，强调 stereo、disparity、pixel-level label 和 point cloud。
- 适用范围：3D 坑洞检测、视差分割、点云验证、几何避障。
- 标注与类别：rgb、disparity、transformed disparity、pixel-level label、point cloud。
- 规模信息：综述中描述该数据集包含 55 组彩色图、亚像素视差图、转换视差图和像素级坑洞标注。
- 项目建议：作为几何方法和深度分割方法的验证集；不建议仅当普通 RGB bbox 数据使用。
- 限制：数据规模较小，但模态丰富；部分文件可能需 Git LFS 或额外下载。
- 推荐引用：*Rethinking Road Surface 3-D Reconstruction and Pothole Detection: From Perspective Transformation to Disparity Map Segmentation*, IEEE Transactions on Cybernetics, 2021。  
  链接：https://www.ruirangerfan.com/projects/tcyb2021-rethinking.html  
  arXiv：https://arxiv.org/abs/2012.10802

## 10. Cracks and Potholes in Road Images Dataset

- 来源：项目页 `https://biankatpas.github.io/Cracks-and-Potholes-in-Road-Images-Dataset/`。
- 作用：道路、裂缝、坑洞联合语义分割。
- 适用范围：道路区域约束、坑洞/裂缝联合分割、背景过滤、可行驶区域辅助判断。
- 标注与类别：每张图像对应 road、crack、pothole 三类二值 PNG mask。
- 项目建议：适合先分割 road 区域，再在道路区域内做 pothole detection/segmentation；可减少非道路背景误检。
- 限制：mask 是按类别分开的二值图，转换 YOLO segment 前需合并或单类转换。
- 推荐引用：数据项目页；在论文中可补充说明访问日期。  
  链接：https://biankatpas.github.io/Cracks-and-Potholes-in-Road-Images-Dataset/

## 11. Multi-Weather Pothole Detection, MWPD

- 来源：Mendeley Data DOI `10.17632/s5hx9n2jc3.2`，公开页面当前可检索到版本 1 DOI `10.17632/s5hx9n2jc3.1`。
- 作用：多天气、多光照坑洞检测。
- 适用范围：正常天气、雨天、白天、黄昏、夜间、小坑洞、部分遮挡坑洞。
- 标注与类别：bbox；类别以 pothole 为主。
- 项目建议：应单独统计 weather/time-of-day 标签；可作为鲁棒性测试集或按天气分层采样。
- 限制：下载后需确认版本号、目录结构和标注格式；若使用 V2，应以下载页实际 DOI 为准。
- 推荐引用：Multi-Weather-based Pothole Detection, Mendeley Data。  
  链接：https://data.mendeley.com/datasets/s5hx9n2jc3/1

## 12. UAV RoadAnomaly-YOLO

- 来源：Mendeley Data DOI `10.17632/c6f2b7mx9t.1`。
- 作用：无人机和地面相机道路异常检测数据集。
- 适用范围：UAV 巡检、跨视角迁移、道路异常多类检测、俯视角坑洞识别。
- 标注与类别：YOLO TXT；包含 alligator cracking、longitudinal crack、transverse crack、rutting、pothole、stripping、raveling、bleeding 等类别。
- 规模信息：Mendeley 页面说明总计 11,024 张图像，划分为 train 8,306、validation 2,012、test 706，统一 640 x 640。
- 项目建议：保留 UAV/ground source 字段；pothole 可抽取为单类，也可保留多类做 road anomaly 检测。
- 限制：跨视角差异大，不应直接与车载近景数据混合而不做 domain 标记。
- 推荐引用：UAV Dataset for Automated Road Surface Degradation Detection in Real-World Conditions, Mendeley Data, DOI `10.17632/c6f2b7mx9t.1`。  
  链接：https://data.mendeley.com/datasets/c6f2b7mx9t/1

## 13. RoadDamageVision

- 来源：Mendeley Data DOI `10.17632/ypm4h4z25c.3`；公开搜索结果可检索到 RoadDamageVision 数据页。
- 作用：道路损伤检测数据，包含 D40 pothole。
- 适用范围：D40 坑洞抽取、道路损伤多类检测、类别不均衡实验、域适应。
- 标注与类别：下载后需确认；配置中按 RDD 风格 D00/D10/D20/D40 管理。
- 项目建议：不要默认和 RDD2020/RDD2022 合并；应先确认类别定义、标注格式和采集域。
- 限制：当前需人工核对版本、许可证和文件格式。
- 推荐引用：RoadDamageVision: Annotated Dataset of Road Damage Images, Mendeley Data。  
  链接：https://data.mendeley.com/datasets/ypm4h4z25c

## 14. Roboflow/Kaggle Pothole Dataset

- 来源：Kaggle `andrewmvd/pothole-detection`。
- 作用：小型 pothole object detection 数据集，适合快速验证流程。
- 适用范围：下载脚本测试、转换脚本冒烟测试、YOLO demo、小规模 baseline。
- 标注与类别：常见为检测标注；下载后应确认是否为 YOLO、COCO 或其他格式。
- 规模信息：项目配置中按约 665 图像的小型数据集处理。
- 项目建议：不要作为主训练数据；适合作为快速可视化和 CI 样例。
- 限制：来源聚合属性较强，许可证和原始来源需核实。
- 推荐引用：Kaggle 数据页。  
  链接：https://www.kaggle.com/datasets/andrewmvd/pothole-detection

## 15. Road Damage Dataset: Potholes, Cracks and Manholes

- 来源：Kaggle `lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes`；相关数据论文为 *Real-world road damage dataset with potholes, cracks, and maintenance holes*。
- 作用：包含坑洞、裂缝、井盖，适合降低井盖被误检为坑洞的问题。
- 适用范围：pothole/crack/manhole 多类检测、hard negative、城市道路误检控制。
- 标注与类别：YOLO object detection；类别为 pothole、crack、manhole。
- 规模信息：论文页面说明该数据集包含 2,009 张标注图像。
- 项目建议：保留 manhole 类，不要简单映射为 background；可显著帮助坑洞 vs 井盖区分。
- 限制：需确认 Kaggle 数据页和论文版本是否完全一致；不同版本可能图像数和格式不同。
- 推荐引用：*Real-world road damage dataset with potholes, cracks, and maintenance holes*。  
  链接：https://pmc.ncbi.nlm.nih.gov/articles/PMC13181123/  
  Kaggle：https://www.kaggle.com/datasets/lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes

## 推荐实验划分

1. 主检测训练：HRP4K + RDD2022 D40 + Water-Filled/Dry + RoadDamagePotholesCracksManholes。
2. 鲁棒性测试：NPD 夜间、MWPD 多天气、Water-Filled/Dry 湿路面。
3. 多模态避障：Pothole-600 + Rui Fan Stereo + Pothole Mix RGB-D clips。
4. 分割任务：UDTIRI + Pothole Mix + Cracks and Potholes in Road Images。
5. hard negative：RDD 裂缝类、manhole 类、HRP4K 负样本、road-only mask 区域。

## 数据治理注意事项

- 许可证先行：Mendeley、Kaggle、GitHub、论文数据页的许可证可能不同，不要把所有数据重新打包公开发布。
- 保留来源字段：统一 manifest 中必须记录 `dataset_name`、`source_url`、`license`、`split`、`annotation_format`。
- 避免泄漏：同一数据集内部可能有近重复帧或视频连续帧，不能只按图像随机切分。
- RDD 映射规则：默认 `D40 -> pothole`；`D00/D10/D20` 可作为 crack/hard negative 或多类训练。
- 分割转检测需谨慎：mask 转 bbox 会损失形状信息；对避障任务应尽量保留 segmentation polygon。
- 深度数据不可丢：Pothole-600、Rui Fan Stereo、Pothole Mix RGB-D 的核心价值在深度/视差，不应只抽 RGB。

## 参考链接

- HRP4K Scientific Data: https://www.nature.com/articles/s41597-026-07317-w
- UDTIRI arXiv: https://arxiv.org/abs/2304.08842
- RDD2022 arXiv: https://arxiv.org/abs/2209.08538
- RDD2020 PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8166755/
- NPD paper: https://www.mdpi.com/2079-9292/13/19/3790
- NPD GitHub: https://github.com/hhaozhang/NPD
- Pothole Mix Mendeley: https://data.mendeley.com/datasets/kfth5g2xk3/2
- Pothole-600: https://sites.google.com/view/pothole-600/dataset
- Rui Fan stereo pothole project: https://www.ruirangerfan.com/projects/tcyb2021-rethinking.html
- Rui Fan arXiv: https://arxiv.org/abs/2012.10802
- Cracks and Potholes in Road Images: https://biankatpas.github.io/Cracks-and-Potholes-in-Road-Images-Dataset/
- MWPD Mendeley: https://data.mendeley.com/datasets/s5hx9n2jc3/1
- UAV RoadAnomaly Mendeley: https://data.mendeley.com/datasets/c6f2b7mx9t/1
- RoadDamageVision Mendeley: https://data.mendeley.com/datasets/ypm4h4z25c
- Kaggle pothole detection: https://www.kaggle.com/datasets/andrewmvd/pothole-detection
- Road damage potholes/cracks/manholes paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC13181123/
