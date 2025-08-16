# 修改打包替换后启动utools进行测试
$dataArray = @("C:\Users\xiaoyu\Desktop", "C:\Users\xiaoyu")
$jsonData = $dataArray | ConvertTo-Json
$response = Invoke-WebRequest -Uri "http://localhost:3000/api/addLocalOpen" -Method POST -Body $jsonData -ContentType "application/json; charset=utf-8"
$response.Content