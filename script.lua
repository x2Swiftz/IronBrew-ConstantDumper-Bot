file = io.open("constants.txt", "w+")

io.output(file)


local old = table.concat
table.concat = function(...)
  local res = old(...)
  io.write(res.."\n")
  return res
end
pcall(function()

--here


end)
io.close(file)