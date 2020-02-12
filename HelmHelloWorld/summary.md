# Helm Hello World

Goal of this one was just to prove that helm can be a useful way to do the sane defaults that can be overridden. This is the config management dream :).

# Sane defaults:

```
$ helm install --dry-run --debug helloworld ./helloworld-chart/ | grep replicas
install.go:149: [debug] Original chart version: ""
install.go:166: [debug] CHART PATH: /Users/aalexander/sandbox/ProofOfConcepts/HelmHelloWorld/helloworld-chart

  replicas: 5
```

# Override file:
```
$ helm install --dry-run --debug -f override.yaml helloworld ./helloworld-chart/ | grep replicas
install.go:149: [debug] Original chart version: ""
install.go:166: [debug] CHART PATH: /Users/aalexander/sandbox/ProofOfConcepts/HelmHelloWorld/helloworld-chart

  replicas: 2
 ```

