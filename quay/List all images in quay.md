通过脚本查询quay中的所有镜像

```
#!/bin/bash
export USER_TOKEN="79X6231CO2QO54ZSO497QQ0VLRJ9AMIP4UCGZ7AL4SK07USEPOJA2TNW6NH3EQVNEGHS7D3C7IHZ65Z0ZQGPFBFFE3QJJVSG6YFYTPFKACVRJWTCOTMR9S2Q"
export QUAY_URL='https://example-registry-quay-quay-enterprise.apps.yawei.example.com'

# 获取所有公共仓库列表
REPOSITORIES=$(curl -ks -H "Authorization: Bearer ${USER_TOKEN}" "${QUAY_URL}/api/v1/repository?public=true")

# 提取命名空间和仓库名称，并处理每个仓库
echo "$REPOSITORIES" | jq -r '.repositories | map(select(.namespace != null and .name != null)) | .[] | "\(.namespace) \(.name)"' | while read -r NS REPO; do

    # 获取当前仓库的所有标签
    TAGS=$(curl -ks -H "Authorization: Bearer ${USER_TOKEN}" "${QUAY_URL}/api/v1/repository/${NS}/${REPO}/tag/" | jq -r '.tags | map(select(.name != null)) | .[].name')
    
    if [ -n "$TAGS" ]; then
        # 显示仓库名称（彩色输出）
        echo -e "\n\033[1;36m仓库名称: ${NS}/${REPO}\033[0m"
        
        # 显示镜像地址列表
        for TAG in $TAGS; do
            IMAGE_URI="${QUAY_URL}/${NS}/${REPO}:${TAG}"
            echo "  └─ ${IMAGE_URI}"
        done
    fi
done
```