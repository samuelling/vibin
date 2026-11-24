# vibin’: every prompt, in order

Things to say to Claude, from https://linglab.org/vibin/. Fill in anything in [brackets].
Each block is one message. Send it, look at what comes back, then go on.


## The short way

> Read https://linglab.org/vibin/VIBIN.md and be my guide through it. I’m new to this. Start at step 2, go one step at a time, and wait for me before moving on.


## Step 2: first demo

> Make me a single web page called gabor.html that shows a Gabor patch on a gray background, with sliders for contrast, spatial frequency, orientation and size. No libraries, just the one file. Then open it in my browser.


## Step 2: change it

> Make it drift, and add a slider for speed.

> Add a second patch next to it. Let me press the left or right arrow to say which one has higher contrast, and keep score.

> The sliders are too small. Make everything bigger and easier to read.


## Step 3: the loop

> Explain what you just built, like I’m a new grad student. Which file does what?

> Before you build anything, tell me your plan in five lines and wait for my OK.

> That’s not right. Here’s what I see: [describe it, or paste the error]. What are the likely causes? Check them before changing anything.


## Step 4: set up git

> I’ve never used git. Set it up for this folder: check that git is installed (help me install it if it isn’t), set my name and email, and save a first checkpoint. Tell me in one sentence what each thing you do is for.


## Step 4: everyday git

> Save a checkpoint.

> What’s changed since the last checkpoint?

> I don’t like where this went. Take me back to the last checkpoint.

> Show me the history as a short list.


## Step 5: put it online

> I have a GitHub account, username [yours]. Connect this computer to it: install the GitHub command-line tool (gh) if it’s missing and walk me through signing in. I’ll do the browser part myself. Then make a new public repo called gabor-demo from this folder, push it, and turn on GitHub Pages so I get a link I can send to someone. Rename gabor.html to index.html if the link needs that.


## Step 6: look at the data

> There’s a file in data/. Don’t change it. Look at it and tell me what’s in it: the columns, how many rows, and anything odd, like missing values or ranges that don’t make sense. Then stop.


## Step 6: first analysis

> Write a Python script that reads that file and plots [what you want: say, mean response for each condition, with error bars across subjects]. Save the figure in figures/. Print the numbers behind the figure so I can check them. Then run it and show me the figure.


## Step 6: check it

> What assumptions did you make in that analysis? List them. Then tell me one way I could check the result by hand.


## Step 7: build the door

> I have an account on BU’s SCC. My login name is [yours]. Set up the file ~/.ssh/config on this computer so that “ssh scc” connects to scc1.bu.edu and keeps one shared connection open for 12 hours (ControlMaster), so I only log in once a day. Back up my existing config first. Don’t try to log in for me: tell me the one command to run, and I’ll type my password and approve Duo myself.


## Step 7: look around

> Check that my SCC connection is open (ssh -O check scc). Then look around, read-only: where is my home directory, which projects am I in, where is my project space, and how full is it? Change nothing.


## Step 7: ground rules

> Download https://linglab.org/vibin/kit/CLAUDE-starter.md. Fill in what you just learned about my SCC setup, ask me about anything you can’t work out, and save it as CLAUDE.md in this folder.


## Step 8: first job

> Download https://linglab.org/vibin/kit/hello.qsub. Put it in a new folder called vibin-practice in my project space on the SCC, fill in my project name, and submit it. Watch the queue until it finishes, then show me what it printed. Explain qsub, qstat and the output file in one sentence each.


## Step 9: set up the practice analysis

> Download https://linglab.org/vibin/vibin-kit.zip and unzip it here. Read the three Python files and the two .qsub files and tell me in plain words what each one does. Then copy them to my vibin-practice folder on the SCC and run make_toy_data.py there.


## Step 9: one subject

> Fill in my project name in analysis.qsub. Submit it for the first subject only, as a test. When it’s done, show me the log and the fitted values. Do they look sensible for a contrast response function?


## Step 9: everyone

> That looks right. Submit all the subjects as an array job. Tell me when they’ve finished and whether any failed. If one failed, read its log and tell me why before you fix anything.


## Step 9: gather

> Fill in my project name in summarize.qsub and submit it. When it’s done, copy just the summary table and the figure back here, into results/ and figures/. Show me the figure and read me the known-answer check.


## Step 10: survey

> My data for [study] is on the SCC at [/projectnb/yourproject/…]. Survey it, read-only: the folder structure, how many subjects, the file types and sizes, and anything that’s inconsistent across subjects. Don’t copy data to this computer. Write what you find to notes/data-map.md here, and add the short version to CLAUDE.md.


## Step 10: plan

> Here’s the analysis I want, in plain words: [for each subject, do this… then across subjects, compare that…]. Don’t write code yet. Give me a plan: which scripts, which jobs, roughly how long and how much memory, and where the outputs go. Tell me what you’re unsure about. Wait for my OK.


## Step 10: one subject

> OK. Do one subject. Show me its output and a quick picture of it, then stop.


## Step 10: known answer

> Before we run everyone: simulate data where we know the true answer, run this same analysis on it, and show me that it recovers the truth. If it doesn’t, say so plainly.


## Step 10: everyone

> Run all subjects as an array job. When it’s done: which failed and why, then the group figure and the table behind it, copied back here. Save a checkpoint.
