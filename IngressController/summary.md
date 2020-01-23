# Ingress Controller POC


# Goal

To have a method by which we can direct traffic into a cluster with the minimum cost and complexity.  IngressControllers are a type of object k8s uses to reuse resources such as loadbalancers, while still keeping the ability for particular paths or domains to be routed to a correct container.

# Requirements

Must allow sub domain based routing.  (a.thing.com -> some set of containers, b.thing.com -> some different set of containers).
Must allow certs to be attached. (ACM/GCP equivalent.)
  Would be quite nice for the demo-sites use case to automatically generate let's encrypt certs, and install them.
Should be entirely contained within k8s.
Should manage dns names

# Optimization goals

Secure.
Stability/reliabilty/uptime.
Cost. (this is why 1 loadbalancer is better than many lbs)
As simple/straight forward as possible.


### The Proof Of Concept

##### Why Voyager?

Seems to handle the let's encrypt piece.  Seems to handle subdomain based routing. Is fully contained within k8s + aws.  May need to install kube2iam or something similar, but that shouldn't be too much trouble.

##### Voyager setup

###### Pre-reqs

Given some k8s cluster. (I built one for this test using kops 1.15.0, k8s version 1.15.6)

Create Some AWS Identity Resources. I ended up adding this inline policy to the k8s nodes role that already existed.

This will enable both voyager and external dns to work.  Voyager uses dns validation for cert creation.  External dns makes/manages records directly in AWS.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:Get*",
                "route53:List*",
                "route53:TestDNSAnswer"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "Stmt1579563999096",
            "Action": "route53:*",
            "Effect": "Allow",
            "Resource": "arn:aws:route53:::hostedzone/<our hosted zone>"
        }
    ]
}
```

##### Once Per cluster setup


Deploy the voyager resources.  I ended up using helm.  The script is in VoyagerSetup, VoyagerViaHelm/setup.sh.  This ends up adding a couple of new CRDs (custom resource definitions) and a deployment of haproxy pods.  The CRDs handle cert requests to let's encrypt, and alb creation.

Before you create the voyager resources in VoyagerUse add a secret with your email like this -- 
`kubectl create secret generic acme-account --from-literal=ACME_EMAIL=exampleperson@example.com`
Then the cert resource will work correctly. Let's Encrypt requires an email for the cert you're generating.

Deploy the external dns resources. Script is in VoyagerSetup/External-DNSViaHelm/setup.sh.  This allows the voyager ingress object to have dns annotations set, and then those records will be created, pointing at the alb. 

##### The examples

I created a couple of simple services, using some off the shelf containers.  There's a nice echo container, that when called via http just gives you back the info of who is calling it (user agent, ip address, etc.)

And the hello service, as 02serviceb.yml.  Which just returns a nice hello page.

Then a cert object, that does the magic of getting a let's encrypt cert and puts it in a secret. I ended up requesting a wildcard cert, but there's no particular reason you couldn't put a bunch of names in the cert, or make a cert for each subdomain etc.

Then, the most interesting part of this PoC, the ingress controller. Some little gotchas, like tls only works if you define a host.  The single domain to single container thing is easiest to see with 06ingressb.yaml file.  ALBs are 1-1 with the object, so each of 05/06 creates a seperate alb.  It's loosely coupled to the service and deployment objects, so multiple dns or albs can point at the same pods.

# Findings

It works!
There are a few little hurdles to handle.  Mostly that multiple deployments of stuff like demo sites will have to manage the same yaml.
Also, that we want external dns to fully manage the dns records, and by default it's set to upsert only.
But, pretty straight forward otherwise.

