(g => {
    var h, a, k, p = "The Google Maps JavaScript API", c = "google", l = "importLibrary", q = "__ib__", 
    m = document, b = window;
    b = b[c] || (b[c] = {});
    var d = b.maps || (b.maps = {}), r = new Set, e = new URLSearchParams, 
    u = () => h || (h = new Promise(async (f, n) => {
        await (a = m.createElement("script"));
        e.set("libraries", [...r] + "");
        for (k in g) 
            e.set(k.replace(/[A-Z]/g, t => "_" + t[0].toLowerCase()), g[k]);
        e.set("callback", c + ".maps." + q);
        a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
        d[q] = f;
        a.onerror = () => h = n(Error(p + " could not load."));
        a.nonce = m.querySelector("script[nonce]")?.nonce || "";
        m.head.append(a);
    }));
    d[l] ? console.warn(p + " only loads once. Ignoring:", g) : d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n));
})({
    key: "AIzaSyDUV3CCdHehd1E-s1KwmPbbt-FcWqMObZ8",
    v: "weekly",
    libraries: ["marker"],
});

// Initialize and add the map
async function initMap() {
    // The location of Dublin
    const position = { lat: 53.3498, lng: -6.2603 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: position,
        mapId: "ebb6cf6a252364a4",
        fullscreenControl: false,
        mapTypeControl: false,
        streetViewControl: false,
        zoomControl: false,
        disableDefaultUI: true,
    });

    placeMarkers(map);  // Calling function for markers once map initialized
}

// Array of stations with random available property
const stations = [
    { name: "MOUNT STREET LOWER", latitude: 53.33796, longitude: -6.24153, available: 10 },
    { name: "CHRISTCHURCH PLACE", latitude: 53.343368, longitude: -6.27012, available: 15 },
    { name: "GRANTHAM STREET", latitude: 53.334123, longitude: -6.265436, available: 4 },
    { name: "PEARSE STREET", latitude: 53.344304, longitude: -6.250427, available: 20 },
    { name: "YORK STREET EAST", latitude: 53.338755, longitude: -6.262003, available: 6 },
    { name: "EXCISE WALK", latitude: 53.347777, longitude: -6.244239, available: 3 },
    { name: "FITZWILLIAM SQUARE WEST", latitude: 53.336074, longitude: -6.252825, available: 16 },
    { name: "PORTOBELLO ROAD", latitude: 53.330091, longitude: -6.268044, available: 3  },
    { name: "PARNELL STREET", latitude: 53.350929, longitude: -6.265125 },
    { name: "FREDERICK STREET SOUTH", latitude: 53.341515, longitude: -6.256853 },
    { name: "FOWNES STREET UPPER", latitude: 53.344603, longitude: -6.263371, available: 3  },
    { name: "CLARENDON ROW", latitude: 53.340927, longitude: -6.262501 },
    { name: "CUSTOM HOUSE", latitude: 53.348279, longitude: -6.254662, available: 6  },
    { name: "RATHDOWN ROAD", latitude: 53.35893, longitude: -6.280337, available: 3  },
    { name: "NORTH CIRCULAR ROAD (O'CONNELL'S)", latitude: 53.357841, longitude: -6.251557 },
    { name: "HANOVER QUAY", latitude: 53.344115, longitude: -6.237153, available: 6  },
    { name: "OLIVER BOND STREET", latitude: 53.343893, longitude: -6.280531 },
    { name: "COLLINS BARRACKS MUSEUM", latitude: 53.347477, longitude: -6.28525 },
    { name: "BROOKFIELD ROAD", latitude: 53.339005, longitude: -6.300217 },
    { name: "BENSON STREET", latitude: 53.344153, longitude: -6.233451, available: 6  },
    { name: "EARLSFORT TERRACE", latitude: 53.334295, longitude: -6.258503, available: 3  },
    { name: "GOLDEN LANE", latitude: 53.340803, longitude: -6.267732, available: 6  },
    { name: "DEVERELL PLACE", latitude: 53.351464, longitude: -6.255265 },
    { name: "WILTON TERRACE (PARK)", latitude: 53.333653, longitude: -6.248345 },
    { name: "JOHN STREET WEST", latitude: 53.343105, longitude: -6.277167, available: 3  },
    { name: "FENIAN STREET", latitude: 53.341428, longitude: -6.24672, available: 6  },
    { name: "MERRION SQUARE SOUTH", latitude: 53.338614, longitude: -6.248606, available: 3  },
    { name: "SOUTH DOCK ROAD", latitude: 53.341833, longitude: -6.231291 },
    { name: "CITY QUAY", latitude: 53.346637, longitude: -6.246154 },
    { name: "EXCHEQUER STREET", latitude: 53.343034, longitude: -6.263578, available: 3  },
    { name: "THE POINT", latitude: 53.346867, longitude: -6.230852, available: 6  },
    { name: "BROADSTONE", latitude: 53.3547, longitude: -6.272314 },
    { name: "HATCH STREET", latitude: 53.33403, longitude: -6.260714, available: 6  },
    { name: "LIME STREET", latitude: 53.346026, longitude: -6.243576 },
    { name: "CHARLEMONT PLACE", latitude: 53.330662, longitude: -6.260177, available: 6  },
    { name: "KILMAINHAM GAOL", latitude: 53.342113, longitude: -6.310015, available: 6  },
    { name: "HARDWICKE PLACE", latitude: 53.357043, longitude: -6.263232 },
    { name: "WOLFE TONE STREET", latitude: 53.348875, longitude: -6.267459, available: 6  },
    { name: "FRANCIS STREET", latitude: 53.342081, longitude: -6.275233 },
    { name: "GREEK STREET", latitude: 53.346874, longitude: -6.272976, available: 6  },
    { name: "GUILD STREET", latitude: 53.347932, longitude: -6.240928, available: 3  },
    { name: "HERBERT PLACE", latitude: 53.334432, longitude: -6.245575 },
    { name: "HIGH STREET", latitude: 53.343565, longitude: -6.275071, available: 6  },
    { name: "NORTH CIRCULAR ROAD", latitude: 53.359624, longitude: -6.260348 },
    { name: "WESTERN WAY", latitude: 53.354929, longitude: -6.269425 },
    { name: "TALBOT STREET", latitude: 53.350974, longitude: -6.25294, available: 6  },
    { name: "NEWMAN HOUSE", latitude: 53.337132, longitude: -6.26059, available: 3  },
    { name: "SIR PATRICK DUN'S", latitude: 53.339218, longitude: -6.240642 },
    { name: "NEW CENTRAL BANK", latitude: 53.347122, longitude: -6.234749, available: 6  },
    { name: "GRANGEGORMAN LOWER (CENTRAL)", latitude: 53.355173, longitude: -6.278424 },
    { name: "KING STREET NORTH", latitude: 53.350291, longitude: -6.273507 },
    { name: "KILLARNEY STREET", latitude: 53.354845, longitude: -6.247579, available: 6  },
    { name: "HERBERT STREET", latitude: 53.335742, longitude: -6.24551 },
    { name: "HANOVER QUAY EAST", latitude: 53.343653, longitude: -6.231755, available: 3  },
    { name: "CUSTOM HOUSE QUAY", latitude: 53.347884, longitude: -6.248048 },
    { name: "MOLESWORTH STREET", latitude: 53.341288, longitude: -6.258117, available: 6  },
    { name: "GEORGES QUAY", latitude: 53.347508, longitude: -6.252192 },
    { name: "KILMAINHAM LANE", latitude: 53.341805, longitude: -6.305085, available: 6  },
    { name: "MOUNT BROWN", latitude: 53.341645, longitude: -6.29719 },
    { name: "MARKET STREET SOUTH", latitude: 53.342296, longitude: -6.287661 },
    { name: "KEVIN STREET", latitude: 53.337757, longitude: -6.267699, available: 3  },
    { name: "ECCLES STREET EAST", latitude: 53.358115, longitude: -6.265601, available: 6  },
    { name: "GRAND CANAL DOCK", latitude: 53.342638, longitude: -6.238695, available: 6  },
    { name: "MERRION SQUARE EAST", latitude: 53.339434, longitude: -6.246548 },
    { name: "YORK STREET WEST", latitude: 53.339334, longitude: -6.264699, available: 6  },
    { name: "ST. STEPHEN'S GREEN SOUTH", latitude: 53.337494, longitude: -6.26199 },
    { name: "DENMARK STREET GREAT", latitude: 53.35561, longitude: -6.261397 },
    { name: "ROYAL HOSPITAL", latitude: 53.343897, longitude: -6.29706, available: 3  },
    { name: "HEUSTON STATION (CAR PARK)", latitude: 53.346985, longitude: -6.297804, available: 6  },
    { name: "GRANGEGORMAN LOWER (NORTH)", latitude: 53.355954, longitude: -6.278378 },
    { name: "ST. STEPHEN'S GREEN EAST", latitude: 53.337824, longitude: -6.256035, available: 3  },
    { name: "HEUSTON STATION (CENTRAL)", latitude: 53.346603, longitude: -6.296924, available: 6  },
    { name: "TOWNSEND STREET", latitude: 53.345922, longitude: -6.254614 },
    { name: "GEORGES LANE", latitude: 53.35023, longitude: -6.279696, available: 6  },
    { name: "PHIBSBOROUGH ROAD", latitude: 53.356307, longitude: -6.273717 },
    { name: "ECCLES STREET", latitude: 53.359246, longitude: -6.269779, available: 3  },
    { name: "PORTOBELLO HARBOUR", latitude: 53.330362, longitude: -6.265163 },
    { name: "MATER HOSPITAL", latitude: 53.359967, longitude: -6.264828 },
    { name: "BLESSINGTON STREET", latitude: 53.356769, longitude: -6.26814, available: 6  },
    { name: "JAMES STREET", latitude: 53.343456, longitude: -6.287409 },
    { name: "MOUNTJOY SQUARE EAST", latitude: 53.356717, longitude: -6.256359, available: 3  },
    { name: "MERRION SQUARE WEST", latitude: 53.339764, longitude: -6.251988 },
    { name: "CONVENTION CENTRE", latitude: 53.34744, longitude: -6.238523 },
    { name: "HARDWICKE STREET", latitude: 53.355473, longitude: -6.264423, available: 3  },
    { name: "PARKGATE STREET", latitude: 53.347972, longitude: -6.291804, available: 6  },
    { name: "SMITHFIELD", latitude: 53.347692, longitude: -6.278214 },
    { name: "DAME STREET", latitude: 53.344007, longitude: -6.266802, available: 6  },
    { name: "HEUSTON BRIDGE (SOUTH)", latitude: 53.347106, longitude: -6.292041 },
    { name: "CATHAL BRUGHA STREET", latitude: 53.352149, longitude: -6.260533, available: 3  },
    { name: "SANDWITH STREET", latitude: 53.345203, longitude: -6.247163 },
    { name: "BUCKINGHAM STREET LOWER", latitude: 53.353331, longitude: -6.249319, available: 6  },
    { name: "ROTHE ABBEY", latitude: 53.338776, longitude: -6.30395 },
    { name: "CHARLEVILLE ROAD", latitude: 53.359157, longitude: -6.281866 },
    { name: "PRINCES STREET / O'CONNELL STREET", latitude: 53.349013, longitude: -6.260311 },
    { name: "UPPER SHERRARD STREET", latitude: 53.358437, longitude: -6.260641, available: 6  },
    { name: "FITZWILLIAM SQUARE EAST", latitude: 53.335211, longitude: -6.2509, available: 3  },
    { name: "GRATTAN STREET", latitude: 53.339629, longitude: -6.243778 },
    { name: "ST JAMES HOSPITAL (LUAS)", latitude: 53.341359, longitude: -6.292951, available: 6  },
    { name: "HARCOURT TERRACE", latitude: 53.332763, longitude: -6.257942 },
    { name: "BOLTON STREET", latitude: 53.351182, longitude: -6.269859 },
    { name: "JERVIS STREET", latitude: 53.3483, longitude: -6.266651, available: 6  },
    { name: "ORMOND QUAY UPPER", latitude: 53.346057, longitude: -6.268001 },
    { name: "GRANGEGORMAN LOWER (SOUTH)", latitude: 53.354663, longitude: -6.278681 },
    { name: "MOUNTJOY SQUARE WEST", latitude: 53.356299, longitude: -6.258586, available: 6  },
    { name: "WILTON TERRACE", latitude: 53.332383, longitude: -6.252717, available: 6  },
    { name: "EMMET ROAD", latitude: 53.340714, longitude: -6.308191, available: 3  },
    { name: "HEUSTON BRIDGE (NORTH)", latitude: 53.347802, longitude: -6.292432 },
    { name: "LEINSTER STREET SOUTH", latitude: 53.34218, longitude: -6.254485 },
    { name: "BLACKHALL PLACE", latitude: 53.3488, longitude: -6.281637 }
  ];

// Function to place markers
function placeMarkers(map) {
    for (const station of stations) {
        const position = { lat: station.latitude, lng: station.longitude };
        let iconUrl;
        // Using for loop and if, else if and else to assign icon colour depending on station availability 
        if (station.available < 5) {
            iconUrl = "Media/bikeRed.png"
        } else if (station.available >= 5 && station.available <= 10) {
            iconUrl = "Media/bikeOrange.png"
        } else {
            iconUrl = "Media/bikeGreen.png"
        }
        const marker = new google.maps.Marker({
            map: map,
            position: position,  
            title: station.name,
            icon: {
                url: iconUrl,  
                scaledSize: new google.maps.Size(25, 25),  // Set size of icon
                anchor: new google.maps.Point(20, 40)  // Center bottom alignment
            }
        });
    }


// Function to create default magnification button 
function createMagControl(map) {
    const magButton = document.createElement("button");
    magButton.className = "defMag"
    magButton.innerHTML = '<img src="Media/magnificationOut.png">';

    magButton.addEventListener("click", () => {
        map.setCenter({ lat: 53.3498, lng: -6.2603 });  // Reset map center to Dublin
        map.setZoom(14); // Reset zoom to default 
    });
    return magButton;
}

const magControlDiv = document.createElement("div");

const magControl = createMagControl(map);

magControlDiv.appendChild(magControl);
map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(magControlDiv);

}
