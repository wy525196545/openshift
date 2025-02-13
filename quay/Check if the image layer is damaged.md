#### If the layer is damaged when pushing the image to the repository, pulling the image will fail.
##### When this problem occurs, you need to check whether the coating is damaged.
- First check the details of the image
```
# skopeo inspect --raw docker://quay.skynet/ibazulic/ubi9/ubi@sha256:c1154105be5991313d18b6d4e7e8c8009c74d4b51ee748872d2b279de15c1af2 | jq '.'
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:4d9d3585895106bd08273429983b91f401339b921cf03c6ecfaaffc8a40b2ad5",
    "size": 5174
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:facf1e7dd3e0c59d3a9c051e50a2263491fd2cbfb31a8c9f6b188bf4af6d85cf",
      "size": 88493018
    },
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:ec465ce79861fa24ca2a402f95f15b884a1c3415778ff7234983bb51befe066c",
      "size": 401
    }
  ],
  "annotations": {
    "org.opencontainers.image.base.digest": "",
    "org.opencontainers.image.base.name": ""
  }
}
```
- Download the image coating that reported an error
```
# mkdir /tmp/test-layer-sha
# cd /tmp/test-layer-sha/
# curl -L "https://quay.skynet/v2/ibazulic/ubi9/ubi/blobs/sha256:facf1e7dd3e0c59d3a9c051e50a2263491fd2cbfb31a8c9f6b188bf4af6d85cf" -o layer.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   625  100   625    0     0   3991      0 --:--:-- --:--:-- --:--:--  3980
100 84.3M  100 84.3M    0     0  95.1M      0 --:--:-- --:--:-- --:--:-- 95.1M
```
- Use sha256sum to check if the layers are consistent
```
# sha256sum layer.tar.gz
facf1e7dd3e0c59d3a9c051e50a2263491fd2cbfb31a8c9f6b188bf4af6d85cf  layer.tar.gz
```
