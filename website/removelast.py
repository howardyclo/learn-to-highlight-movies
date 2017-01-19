def RemoveLastHL(Highlight):
	NewLast = (Highlight[-1][0],-1)
	Highlight.pop()
	Highlight.append(NewLast)
	return Highlight