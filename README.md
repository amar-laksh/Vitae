# Vitae

It is an Esoteric interpreted python-built language on the concept of the ultimate NP-complete problem; Life. Vitae's interpreter is built from scratch without any libraries or frameworks like LLVM etc.

Vitae incorporates dynamic, non-typed, easy to learn design metrics to introduce non-technical people to programming in their lives, telling them about life itself!

**HURRAY TO EASY PROGRAMMING!**

## Usage

In order to run the python file-
```
  python vitae.py -c {filename}
```
For e.g.-

```
  python vitae.py -c examples/first.vit
```


## Examples

Hello the World!-
```
  born
	say "hello world this is the first utterance of vitae!"
  die
```
**Get a thing or two! (Variables)**

Variables(called things in Vitae!), are typed implicitly by the interpreter and are initialized in the following manner!
```
  born
	thing hello is "Hello World and"
	thing bond is 007
	say hello, bond
  die
```
**Times and Done! (Loops!)**

For the time being Vitae supports a simple looping construct called 'Times / Done'. The following is an example-

```
  born
	thing a is "Hello"
	thing b is "\tWorld"
	10 times
		say a, b
	done
  die
```
**Listening into things!**

We can bound stdin input to any thing(variable) and then use it anywhere!

```
 born
	listen("Please enter your input:\n ") into a
	thing b is 21
	3 times
		say a
		say b
	done  
 die
```

