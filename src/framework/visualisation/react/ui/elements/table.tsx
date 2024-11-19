import { useEffect, useLayoutEffect, useMemo, useRef, useState, ReactNode, Dispatch, SetStateAction } from 'react'
import Highlighter from 'react-highlight-words'
import { TableWithContext, PropsUITableRow } from '../../../../types/elements'
import { CheckBox } from './check_box'

import UndoSvg from '../../../../../assets/images/undo.svg'
import DeleteSvg from '../../../../../assets/images/delete.svg'
import { Pagination } from './pagination'
import TextBundle from '../../../../text_bundle'
import { Translator } from '../../../../translator'

export interface Props {
  table: TableWithContext
  show: boolean
  locale: string
  search: string
  unfilteredRows: number
  handleDelete?: (rowIds: string[]) => void
  handleUndo?: () => void
  pageSize?: number
}

interface Tooltip {
  show: boolean
  content: ReactNode
  x: number
  y: number
}

export const Table = ({
  table,
  show,
  locale,
  search,
  unfilteredRows,
  handleDelete,
  handleUndo,
  pageSize = 7
}: Props): JSX.Element => {
  const [page, setPage] = useState(0)
  const columnNames = table.head.cells
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const ref = useRef<HTMLDivElement>(null)
  const innerRef = useRef<HTMLDivElement>(null)
  const nPages = Math.ceil(table.body.rows.length / pageSize)
  const selectedLabel = selected.size.toLocaleString(locale, { useGrouping: true })
  const text = useMemo(() => getTranslations(locale), [locale])

  const [tooltip, setTooltip] = useState<Tooltip>({
    show: false,
    content: null,
    x: 0,
    y: 0
  })

  const cellClass = 'min-h-[2.1rem] md:min-h-[2.5rem] px-3 flex items-center font-table-row'

  useEffect(() => {
    setSelected(new Set())
    setPage((page) => Math.max(0, Math.min(page, nPages - 1)))
  }, [table, nPages])

  useEffect(() => {
    // rm tooltip on scroll
    function rmTooltip (): void {
      setTooltip((tooltip: Tooltip) => (tooltip.show ? { ...tooltip, show: false } : tooltip))
    }
    window.addEventListener('scroll', rmTooltip)
    return () => window.removeEventListener('scroll', rmTooltip)
  })

  useLayoutEffect(() => {
    // set exact height of grid row for height transition
    if (ref.current == null || innerRef.current == null) return
    if (!show || unfilteredRows === 0) {
      ref.current.style.gridTemplateRows = '0rem'
      return
    }

    function responsiveHeight (): void {
      if (ref.current == null || innerRef.current == null) return
      ref.current.style.gridTemplateRows = `${innerRef.current.scrollHeight}px`
    }
    responsiveHeight()
    // just as a precaution, update height every second in case it changes
    const interval = setInterval(responsiveHeight, 1000)
    return () => clearInterval(interval)
  }, [ref, innerRef, show, nPages, unfilteredRows])

  const items = useMemo(() => {
    const items: Array<PropsUITableRow | null> = new Array(pageSize).fill(null)
    for (let i = 0; i < pageSize; i++) {
      const index = page * pageSize + i
      if (table.body.rows[index] !== undefined) items[i] = table.body.rows[index]
    }
    return items
  }, [table, page, pageSize])

  function renderHeaderCell (value: string, i: number): JSX.Element {
    return (
      <th key={`header ${i}`}>
        <div className={`text-left ${cellClass}`}>
          <div>{value}</div>
        </div>
      </th>
    )
  }

  function renderRow (item: PropsUITableRow | null, i: number): JSX.Element | null {
    if (item == null && i >= unfilteredRows) return null
    if (item == null) {
      return (
        <tr key={`{empty ${i}`} className='border-b-2 border-grey4'>
          <td>
            <div className={cellClass} />
          </td>
        </tr>
      )
    }
    return (
      <tr key={item.id} className='border-b-2 border-grey4 border-solid'>
        {table.deleteOption &&
          (
            <td key='select'>
              <CheckBox
                id={item.id}
                size='w-6 h-6'
                selected={selected.has(item.id)}
                onSelect={() => toggleSelected(item.id)}
              />
            </td>
          )
        }

        {item.cells.map((cell, j) => (
          <td key={j}>
            <Cell cell={cell} search={search} cellClass={cellClass} setTooltip={setTooltip} />
          </td>
        ))}
      </tr>
    )
  }

  function toggleSelected (id: string): void {
    if (selected.has(id)) {
      selected.delete(id)
    } else {
      selected.add(id)
    }
    setSelected(new Set(selected))
  }

  function toggleSelectAll (): void {
    if (selected.size === table.body.rows.length) {
      setSelected(new Set())
    } else {
      setSelected(new Set(table.body.rows.map((row) => row.id)))
    }
  }

  return (
    <div
      ref={ref}
      className='grid grid-cols-1 transition-[grid,color] duration-500 relative overflow-hidden text-sm md:text-base'
    >
      <div ref={innerRef} className={`h-min ${unfilteredRows === 0 ? 'invisible' : ''}`}>
        <div className='my-2 bg-grey6 rounded-md border-grey4 border-[0.2rem]'>
          <div className='p-3 pt-1 pb-2 max-w-full overflow-x-auto'>
            <table className='table-fixed min-w-full '>
              <thead className=''>
                <tr className='border-b-2 border-grey4 border-solid'>
                  {table.deleteOption &&
                    (
                      <td className='w-8'>
                        <CheckBox
                          id='selectAll'
                          size='w-6 h-6'
                          selected={table.body.rows.length > 0 && selected.size === table.body.rows.length}
                          onSelect={toggleSelectAll}
                        />
                      </td>
                    )
                  }
                  {columnNames.map(renderHeaderCell)}
                </tr>
              </thead>
              <tbody>{items.map(renderRow)}</tbody>
            </table>
          </div>
          <div className='px-3 pb-1 flex justify-between min-h-[2.5rem]'>
            <div className='pt-2 pb-2'>
              {selected.size > 0 || table.deletedRowCount === 0
                ? (
                  <IconButton
                    icon={DeleteSvg}
                    label={`${text.delete} ${selected.size > 0 ? selectedLabel : ''}`}
                    color='text-delete'
                    disabled={selected.size === 0}
                    hidden={!table.deleteOption}
                    onClick={() => handleDelete?.(Array.from(selected))}
                  />
                  )
                : (
                  <IconButton icon={UndoSvg} label={text.undo} color='text-primary' onClick={() => handleUndo?.()} />
                  )}
            </div>
            <Pagination page={page} setPage={setPage} nPages={nPages} />
          </div>
        </div>
        <div
          className={`${
            tooltip.show ? '' : 'invisible'
          } break-all fixed bg-[#222a] -translate-x-2 -translate-y-2 p-2  rounded text-white backdrop-blur-[2px] z-20 max-w-[20rem] pointer-events-none overflow-auto font-table-row`}
          style={{ left: tooltip.x, top: tooltip.y } as any}
        >
          {tooltip.content}
        </div>
      </div>
    </div>
  )
}

function Cell ({
  cell,
  search,
  cellClass,
  setTooltip
}: {
  cell: string
  search: string
  cellClass: string
  setTooltip: Dispatch<SetStateAction<Tooltip>>
}): JSX.Element {
  const textRef = useRef<HTMLDivElement>(null)
  const [overflows, setOverflows] = useState(false)
  const isUrl = /^https?:\/\//.test(cell)

  const searchWords = useMemo(() => {
    return [search]
    // return search.split(' ') // alternative: highlight individual words
  }, [search])

  useEffect(() => {
    if (textRef.current == null) return
    setOverflows(textRef.current.scrollWidth > textRef.current.clientWidth)
  }, [textRef])

  function onSetTooltip (): void {
    if (isUrl) return
    if (textRef.current == null) return
    if (!overflows) return

    const rect = textRef.current.getBoundingClientRect()

    const content = (
      <Highlighter
        searchWords={searchWords}
        autoEscape
        textToHighlight={cell}
        highlightClassName='bg-tertiary rounded-sm'
      />
    )

    setTooltip({
      show: true,
      content,
      x: rect.x,
      y: rect.y
    })
  }

  function onRmTooltip (): void {
    setTooltip((tooltip: Tooltip) => (tooltip.show ? { ...tooltip, show: false } : tooltip))
  }

  return (
    <div
      className={`relative ${cellClass}`}
      onMouseEnter={onSetTooltip}
      onMouseLeave={onRmTooltip}
      onClick={onSetTooltip}
    >
      <div ref={textRef} className='whitespace-nowrap max-w-[15rem] overflow-hidden overflow-ellipsis z-10'>
        {isUrl
          ? (
            <a href={cell} className='text-primary' target='_blank' rel='noopener noreferrer'>
              <Highlighter
                searchWords={searchWords}
                autoEscape
                textToHighlight={cell}
                highlightClassName='bg-tertiary rounded-sm'
              />
            </a>
            )
          : (
            <Highlighter
              searchWords={searchWords}
              autoEscape
              textToHighlight={cell}
              highlightClassName='bg-tertiary rounded-sm'
            />
            )}
      </div>
      {overflows && !isUrl && <TooltipIcon />}
    </div>
  )
}

function TooltipIcon (): JSX.Element {
  return (
    <svg
      className='w-3 h-3 mb-1 text-gray-800 dark:text-white'
      aria-hidden='true'
      xmlns='http://www.w3.org/2000/svg'
      fill='none'
      viewBox='0 0 10 16'
    >
      <path
        stroke='currentColor'
        strokeLinecap='round'
        strokeLinejoin='round'
        strokeWidth='2'
        d='m2.707 14.293 5.586-5.586a1 1 0 0 0 0-1.414L2.707 1.707A1 1 0 0 0 1 2.414v11.172a1 1 0 0 0 1.707.707Z'
      />
    </svg>
  )
}

function IconButton (props: {
  icon: string
  label: string
  onClick: () => void
  color: string
  disabled?: boolean
  hidden?: boolean
}): JSX.Element | null {
  if (props.hidden ?? false) return null
  const disabled = props.disabled ?? false
  return (
    <div
      className={`flex items-center gap-2 cursor-pointer  ${props.color} animate-fadeIn md:text-button ${
        disabled ? 'opacity-50' : ''
      }`}
      onClick={() => !disabled && props.onClick()}
    >
      <img src={props.icon} className='w-7 h-7 ml-1 md:w-9 md:h-9 md:ml-0 -translate-x-[3px]' />
      {props.label}
    </div>
  )
}

function getTranslations (locale: string): Record<string, string> {
  const translated: Record<string, string> = {}
  for (const [key, value] of Object.entries(translations)) {
    translated[key] = Translator.translate(value, locale)
  }
  return translated
}

const translations = {
  delete: new TextBundle().add('en', 'Delete').add('nl', 'Verwijder'),
  undo: new TextBundle().add('en', 'Undo').add('nl', 'Herstel')
}
