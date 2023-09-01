rm -rf dist
mkdir -p dist
cd tr-util
yarn build
mv dist ../dist/client
cd ..
cp -r server dist/server
rm dist/server/.env

docker build -t trilium-util:$1 .