import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, act } from "@testing-library/react";
import ItineraryMap from "../components/ItineraryMap.jsx";

// Store the MapLibre mock functions so tests can inspect their calls.
const mocks = vi.hoisted(() => ({
  map: null,
  observer: null,
  bounds: null,
  setWorkerUrl: vi.fn(),
  getVersion: vi.fn(() => "test-version"),
  Map: vi.fn(),
  NavigationControl: vi.fn(),
  LngLatBounds: vi.fn(),
  Popup: vi.fn(),
}));

vi.mock("maplibre-gl", () => ({
  setWorkerUrl: mocks.setWorkerUrl,
  getVersion: mocks.getVersion,
  Map: mocks.Map,
  NavigationControl: mocks.NavigationControl,
  LngLatBounds: mocks.LngLatBounds,
  Popup: mocks.Popup,
}));

const mockCenter = {
  lng: 2.3522,
  lat: 48.8566,
};

const mockStops = [
  {
    id: 10,
    attractionId: 1,
    name: "Eiffel Tower",
    lng: 2.2945,
    lat: 48.8584,
  },
];

const mockAttractions = [
  {
    id: 1,
    name: "Eiffel Tower",
    lng: 2.2945,
    lat: 48.8584,
  },
  {
    id: 2,
    name: "Louvre Museum",
    lng: 2.3376,
    lat: 48.8606,
  },
];

describe("ItineraryMap", () => {
  beforeEach(() => {
    vi.clearAllMocks();

    mocks.Map.mockImplementation(function (options) {
      const map = {
        options,
        handlers: {},
        layerHandlers: {},
        sources: {},

        addControl: vi.fn(),

        on: vi.fn((event, layerOrHandler, handler) => {
          if (handler) {
            map.layerHandlers[`${event}:${layerOrHandler}`] = handler;
          } else {
            map.handlers[event] = layerOrHandler;
          }
        }),

        addSource: vi.fn((name, source) => {
          map.sources[name] = {
            definition: source,
            setData: vi.fn(),
          };
        }),

        getSource: vi.fn((name) => map.sources[name]),

        addLayer: vi.fn(),

        getCanvas: vi.fn(() => ({
          style: { cursor: "" },
        })),

        fitBounds: vi.fn(),
        easeTo: vi.fn(),
        resize: vi.fn(),
        remove: vi.fn(),
      };

      mocks.map = map;

      return map;
    });

    mocks.NavigationControl.mockImplementation(function () {
      return {};
    });

    mocks.LngLatBounds.mockImplementation(function () {
      const bounds = {
        extend: vi.fn(),
      };

      mocks.bounds = bounds;
      return bounds;
    });

    mocks.Popup.mockImplementation(function () {
      return {
        setLngLat: vi.fn().mockReturnThis(),
        setText: vi.fn().mockReturnThis(),
        addTo: vi.fn().mockReturnThis(),
      };
    });

    vi.stubGlobal(
      "ResizeObserver",
      class {
        constructor(callback) {
          this.callback = callback;
          this.observe = vi.fn();
          this.disconnect = vi.fn();
          mocks.observer = this;
        }
      },
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  const triggerMapLoad = () => {
    act(() => {
      mocks.map.handlers.load();
    });
  };

  it("initialises the map using the supplied destination coordinates", () => {
    render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    expect(mocks.Map).toHaveBeenCalledWith(
      expect.objectContaining({
        center: [2.3522, 48.8566],
        zoom: 11,
        style: "https://tiles.openfreemap.org/styles/liberty",
      }),
    );

    expect(mocks.map.addControl).toHaveBeenCalled();
    expect(mocks.observer.observe).toHaveBeenCalled();
  });

  it("uses the fallback centre when destination coordinates are invalid", () => {
    render(
      <ItineraryMap
        center={{ lng: 200, lat: 100 }}
        stops={[]}
        attractions={[]}
      />,
    );

    expect(mocks.Map).toHaveBeenCalledWith(
      expect.objectContaining({
        center: [-2.2431, 51.8642],
      }),
    );
  });

  it("creates the attraction and planned-stop sources and layers when the map loads", () => {
    render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    expect(mocks.map.addSource).toHaveBeenCalledWith(
      "attractions",
      expect.objectContaining({ type: "geojson" }),
    );

    expect(mocks.map.addSource).toHaveBeenCalledWith(
      "stops",
      expect.objectContaining({ type: "geojson" }),
    );

    expect(mocks.map.addLayer).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "attractions-layer",
        source: "attractions",
      }),
    );

    expect(mocks.map.addLayer).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "stops-layer",
        source: "stops",
      }),
    );
  });

  it("excludes scheduled attractions from the available attractions source", () => {
    render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    const attractionSource = mocks.map.sources.attractions;

    expect(attractionSource.setData).toHaveBeenLastCalledWith(
      expect.objectContaining({
        type: "FeatureCollection",
        features: [
          expect.objectContaining({
            properties: {
              id: "2",
              name: "Louvre Museum",
            },
          }),
        ],
      }),
    );
  });

  it("fits the map around multiple scheduled stops", () => {
    const multipleStops = [
      mockStops[0],
      {
        id: 11,
        attractionId: 2,
        name: "Louvre Museum",
        lng: 2.3333,
        lat: 48.8667,
      },
    ];

    render(
      <ItineraryMap
        center={mockCenter}
        stops={multipleStops}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    expect(mocks.LngLatBounds).toHaveBeenCalled();
    expect(mocks.bounds.extend).toHaveBeenCalledTimes(2);

    expect(mocks.map.fitBounds).toHaveBeenCalledWith(mocks.bounds, {
      padding: 60,
      maxZoom: 14,
      duration: 500,
    });
  });

  it("centres the map on a single scheduled stop", () => {
    render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    expect(mocks.map.easeTo).toHaveBeenCalledWith({
      center: [2.2945, 48.8584],
      zoom: 13,
      duration: 500,
    });
  });

  it("updates map sources when the attractions or stops change", () => {
    const { rerender } = render(
      <ItineraryMap
        center={mockCenter}
        stops={[]}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    const stopsSource = mocks.map.sources.stops;
    const initialCallCount = stopsSource.setData.mock.calls.length;

    const updatedStops = [
      {
        id: 10,
        attractionId: 1,
        name: "Roman Baths",
        lng: -2.359,
        lat: 51.381,
      },
    ];

    rerender(
      <ItineraryMap
        center={mockCenter}
        stops={updatedStops}
        attractions={mockAttractions}
      />,
    );

    expect(stopsSource.setData).toHaveBeenCalledTimes(initialCallCount + 1);
    expect(stopsSource.setData).toHaveBeenLastCalledWith(
      expect.objectContaining({
        features: [
          expect.objectContaining({
            properties: {
              id: "10",
              name: "Roman Baths",
            },
          }),
        ],
      }),
    );
  });

  it("opens a popup when a map feature is clicked", () => {
    render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    triggerMapLoad();

    const clickHandler = mocks.map.layerHandlers["click:stops-layer"];

    act(() => {
      clickHandler({
        features: [
          {
            geometry: {
              coordinates: [-2.359, 51.381],
            },
            properties: {
              name: "Roman Baths",
            },
          },
        ],
      });
    });

    expect(mocks.Popup).toHaveBeenCalled();
  });

  it("disconnects the resize observer and removes the map on unmount", () => {
    const { unmount } = render(
      <ItineraryMap
        center={mockCenter}
        stops={mockStops}
        attractions={mockAttractions}
      />,
    );

    const map = mocks.map;
    const observer = mocks.observer;

    unmount();

    expect(observer.disconnect).toHaveBeenCalled();
    expect(map.remove).toHaveBeenCalled();
  });
});
