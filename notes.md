## Connect to docker daemon (every new shell)

```
eval $(docker-machine env vscode-commandsuggestions)
```

## Deploy

```
docker-compose build
docker-compose -f docker-compose.yml up -d
docker-compose logs --tail=100 -f
```

## Setup up docker-machine (only when recreating Docker VM in Azure)

`--engine-install-url` works around issue with latest version of Docker install.

```
docker-machine create --driver azure --azure-dns vscode-commandsuggestions --azure-open-port 80 --azure-ssh-user vscode-commandsuggestions --azure-subscription-id <subscription_id> --azure-location westus --azure-resource-group CommandSuggestions --azure-size Standard_A2_v2 --engine-install-url=https://web.archive.org/web/20170623081500/https://get.docker.com vscode-commandsuggestions
```
