import angr

# Create the angr project
proj = angr.Project('./rev', load_options={"auto_load_libs":False})
initial_state = proj.factory.entry_state() 

# Discard lazy solves to speed up angr
initial_state.options.discard("LAZY_SOLVES")

# Flag is stdin
# Length of user input is 33 bytes
# Specify the first 32 bytes to be neither null nor newlines.
for _ in range(0,32):
	k = initial_state.posix.files[0].read_from(1)
	initial_state.se.add(k != 0)
	initial_state.se.add(k != 10)

# The last char of user input must be a newline
k = initial_state.posix.files[0].read_from(1)
initial_state.se.add(k == 10)

# Reset the stdin to the beginning, 0
initial_state.posix.files[0].seek(0)
initial_state.posix.files[0].length = 33

# Explore the binary 
pg = proj.factory.path_group(initial_state, immutable=False)
pg.explore(find=0x08048681)

# Print what we found
found = pg.found[0].state
found.posix.files[0].seek(0)
print("Found: "+ found.se.any_str(found.posix.files[0].read_from(33)))


