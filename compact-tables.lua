-- Keep short data tables at their natural width in the HTML ebook.
function Table(tbl)
  if not FORMAT:match('html') or #tbl.colspecs > 3 then return end
  local rows = {}
  for _, row in ipairs(tbl.head.rows) do rows[#rows + 1] = row end
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.head) do rows[#rows + 1] = row end
    for _, row in ipairs(body.body) do rows[#rows + 1] = row end
  end
  for _, row in ipairs(tbl.foot.rows) do rows[#rows + 1] = row end
  if #rows < 2 or #rows > 8 then return end
  for _, row in ipairs(rows) do
    for _, cell in ipairs(row.cells) do
      if #pandoc.utils.stringify(cell.contents) > 48 then return end
    end
  end
  tbl.classes:insert('compact-data-table')
  return tbl
end
