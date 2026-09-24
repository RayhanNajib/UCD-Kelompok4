import { createRoot } from 'react-dom/client'
import { Tldraw } from 'tldraw'
import 'tldraw/tldraw.css'
import React, { useEffect } from 'react'

function App() {
  const handleMount = (editor) => {
    // Populate research nodes into official tldraw SDK canvas programmatically!
    editor.createShapes([
      // Title Label
      {
        id: 'shape:title',
        type: 'geo',
        x: 100,
        y: 50,
        props: {
          w: 800,
          h: 80,
          geo: 'rectangle',
          color: 'violet',
          fill: 'solid',
          text: '🧵 PAPAN BRAINSTORMING UCD (OFFICIAL TLDRAW SDK)\nStudi Kasus TransAgro & TaniFresh — Kelompok 4',
          font: 'sans',
          align: 'middle'
        }
      },
      // Problem Node 1 (BPS)
      {
        id: 'shape:bps',
        type: 'geo',
        x: 100,
        y: 180,
        props: {
          w: 360,
          h: 220,
          geo: 'rectangle',
          color: 'red',
          fill: 'semi',
          text: '🔴 DATA MASALAH 1 (BPS JATIM 2025)\n\n• MPP (Margin Perdagangan) 42.65% - 58.10%\n• Rantai 4-5 tengkulak di Jatim.\n• Harga cabai/tomat di kebun Rp 12.000/kg, di konsumen Rp 35.000/kg.',
          align: 'start'
        }
      },
      // Problem Node 2 (Kementan)
      {
        id: 'shape:kementan',
        type: 'geo',
        x: 100,
        y: 450,
        props: {
          w: 360,
          h: 220,
          geo: 'rectangle',
          color: 'orange',
          fill: 'semi',
          text: '🔴 DATA MASALAH 2 (KEMENTAN RI)\n\n• Post-Harvest Loss (Kerusakan Pasca Panen): 20% - 35%.\n• Cold-chain buruk & durasi transit pengangkut sayur terlalu lama di rute pegunungan.',
          align: 'start'
        }
      },
      // Geo Node (BMKG & Maps)
      {
        id: 'shape:geo',
        type: 'geo',
        x: 520,
        y: 300,
        props: {
          w: 360,
          h: 220,
          geo: 'rectangle',
          color: 'yellow',
          fill: 'semi',
          text: '🗺️ GEOGRAFIS & RUTE PUJON - MALANG\n\n• BMKG: Curah hujan ekstrem 100-120mm/jam.\n• Jalur 38.5 km rawan longsor/terputus (DetikNews).\n• Google Maps: Pujon (-7.8427, 112.4673)',
          align: 'start'
        }
      },
      // User Persona (Bambang Hariyadi)
      {
        id: 'shape:persona',
        type: 'geo',
        x: 940,
        y: 180,
        props: {
          w: 360,
          h: 240,
          geo: 'rectangle',
          color: 'green',
          fill: 'semi',
          text: '👤 USER PERSONA: PAK BAMBANG (45 TH)\nKoordinator Logistik Sayur Pujon Malang\n\n• Goals: Kerusakan < 5%, rute aman hujan.\n• Pain Points: Kerusakan 35% di rute, penentuan jam berangkat manual (10m).',
          align: 'start'
        }
      },
      // Solution 1 (TaniFresh)
      {
        id: 'shape:sol1',
        type: 'geo',
        x: 1360,
        y: 150,
        props: {
          w: 380,
          h: 220,
          geo: 'rectangle',
          color: 'light-green',
          fill: 'semi',
          text: '🌱 SOLUSI 1: TaniFresh-Express\n(Direct Micro-Distribution)\n\n• Menghubungkan petani Pujon ke konsumen kota tanpa perantara.\n• Pengiriman terdekat berbasis zona & eco-packaging.',
          align: 'start'
        }
      },
      // Solution 2 (TransAgro - Utama)
      {
        id: 'shape:sol2',
        type: 'geo',
        x: 1360,
        y: 430,
        props: {
          w: 380,
          h: 240,
          geo: 'rectangle',
          color: 'blue',
          fill: 'semi',
          text: '🚛 SOLUSI 2: TransAgro Spoilage-Route\n(Utama Kelompok 4 • Logistics Risk Engine)\n\n• Integrasi Weather Engine BMKG.\n• Urutkan prioritas keberangkatan armada & kalkulasi risiko pembusukan otomatis (10m -> 2m).',
          align: 'start'
        }
      }
    ])

    // Create Connecting Arrows (Red Strings)
    editor.createShapes([
      {
        id: 'shape:arrow1',
        type: 'arrow',
        x: 460,
        y: 290,
        props: {
          start: { x: 0, y: 0 },
          end: { x: 480, y: 0 },
          color: 'red',
          text: 'Monopoli Tengkulak'
        }
      },
      {
        id: 'shape:arrow2',
        type: 'arrow',
        x: 880,
        y: 350,
        props: {
          start: { x: 0, y: 0 },
          end: { x: 60, y: -80 },
          color: 'red',
          text: 'Risiko Cuaca Pujon'
        }
      },
      {
        id: 'shape:arrow3',
        type: 'arrow',
        x: 1300,
        y: 250,
        props: {
          start: { x: 0, y: 0 },
          end: { x: 60, y: 0 },
          color: 'green',
          text: 'Potong Perantara'
        }
      },
      {
        id: 'shape:arrow4',
        type: 'arrow',
        x: 1300,
        y: 320,
        props: {
          start: { x: 0, y: 0 },
          end: { x: 60, y: 200 },
          color: 'blue',
          text: 'Weather Engine & Armada'
        }
      }
    ])
  }

  return (
    <div style={{ position: 'fixed', inset: 0 }}>
      <Tldraw onMount={handleMount} />
    </div>
  )
}

const root = createRoot(document.getElementById('root'))
root.render(<App />)
