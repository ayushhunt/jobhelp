'use client'

import { useEffect, useRef } from 'react'
import * as d3 from 'd3'
import cloud from 'd3-cloud'

interface WordCloudProps {
  words: { text: string; value: number }[]
  type: 'resume' | 'jd'
}

export default function WordCloud({ words, type }: WordCloudProps) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!svgRef.current || words.length === 0) return

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove()

    const width = 400
    const height = 300

    // Scale word sizes between 10 and 50 based on frequency
    const fontSize = d3.scaleLinear()
      .domain([
        d3.min(words, d => d.value) || 1,
        d3.max(words, d => d.value) || 1
      ])
      .range([12, 40])

    // Generate word cloud layout
    const layout = cloud()
      .size([width, height])
      .words(words)
      .padding(3)
      .rotate(() => 0)
      .fontSize(d => fontSize(d.value))
      .on("end", draw)

    layout.start()

    function draw(words: d3.cloud.Word[]) {
      const svg = d3.select(svgRef.current)
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2},${height / 2})`)

      svg.selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", d => `${d.size}px`)
        .style("font-family", "Inter var, sans-serif")
        .style("fill", () => type === 'resume' ? 'rgb(59, 130, 246)' : 'rgb(147, 51, 234)')
        .style("opacity", d => (d.size || 0) / 40)
        .attr("text-anchor", "middle")
        .attr("transform", d => `translate(${d.x},${d.y})`)
        .text(d => d.text)
    }
  }, [words, type])

  return (
    <div className="w-full h-full flex items-center justify-center">
      <svg ref={svgRef} className="w-full h-full" />
    </div>
  )
}
